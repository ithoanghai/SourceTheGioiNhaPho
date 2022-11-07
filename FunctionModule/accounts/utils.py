import unicodedata
import string
import re
import random
from collections import OrderedDict
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.core.validators import validate_email
from django.db import models
from django.db.models import Q, EmailField
from django.http import HttpResponseRedirect
from django.utils.encoding import force_str
from django.utils.http import base36_to_int, int_to_base36, urlencode
from django.utils.timezone import now

from TownhouseWorldRealestate.exceptions import ImmediateHttpResponse
from TownhouseWorldRealestate.utils import (
    get_request_param,
    import_callable,
)
from . import app_settings, signals
from .adapter import get_adapter


def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    norm_s1 = unicodedata.normalize("NFKC", s1).casefold()
    norm_s2 = unicodedata.normalize("NFKC", s2).casefold()
    return norm_s1 == norm_s2


def get_next_redirect_url(request, redirect_field_name="next"):
    """
    Returns the next URL to redirect to, if it was explicitly passed
    via the request.
    """
    redirect_to = get_request_param(request, redirect_field_name)
    if not get_adapter(request).is_safe_url(redirect_to):
        redirect_to = None
    return redirect_to


def get_login_redirect_url(request, url=None, redirect_field_name="next", signup=False):
    ret = url
    if url and callable(url):
        # In order to be able to pass url getters around that depend
        # on e.g. the authenticated state.
        ret = url()
    if not ret:
        ret = get_next_redirect_url(request, redirect_field_name=redirect_field_name)
    if not ret:
        if signup:
            ret = get_adapter(request).get_signup_redirect_url(request)
        else:
            ret = get_adapter(request).get_login_redirect_url(request)
    return ret


_user_display_callable = None


def logout_on_password_change(request, user):
    # Since it is the default behavior of Django to invalidate all sessions on
    # password change, this function actually has to preserve the session when
    # logout isn't desired.
    if not app_settings.LOGOUT_ON_PASSWORD_CHANGE:
        update_session_auth_hash(request, user)


def default_user_display(user):
    if app_settings.USER_MODEL_USERNAME_FIELD:
        return getattr(user, app_settings.USER_MODEL_USERNAME_FIELD)
    else:
        return force_str(user)


def user_display(user):
    global _user_display_callable
    if not _user_display_callable:
        f = getattr(settings, "ACCOUNT_USER_DISPLAY", default_user_display)
        _user_display_callable = import_callable(f)
    return _user_display_callable(user)


def user_field(user, field, *args):
    """
    Gets or sets (optional) user model fields. No-op if fields do not exist.
    """
    if not field:
        return
    User = get_user_model()
    try:
        field_meta = User._meta.get_field(field)
        max_length = field_meta.max_length
    except FieldDoesNotExist:
        if not hasattr(user, field):
            return
        max_length = None
    if args:
        # Setter
        v = args[0]
        if v:
            v = v[0:max_length]
        setattr(user, field, v)
    else:
        # Getter
        return getattr(user, field)


def user_username(user, *args):
    if args and not app_settings.PRESERVE_USERNAME_CASING and args[0]:
        args = [args[0].lower()]
    return user_field(user, app_settings.USER_MODEL_USERNAME_FIELD, *args)


def user_email(user, *args):
    return user_field(user, app_settings.USER_MODEL_EMAIL_FIELD, *args)


def _has_verified_for_login(user, email):
    from .models import EmailAddress

    emailaddress = None
    if email:
        ret = False
        try:
            emailaddress = EmailAddress.objects.get_for_user(user, email)
            ret = emailaddress.verified
        except EmailAddress.DoesNotExist:
            pass
    else:
        ret = EmailAddress.objects.filter(user=user, verified=True).exists()
    return ret


def perform_login(
    request,
    user,
    email_verification,
    redirect_url=None,
    signal_kwargs=None,
    signup=False,
    email=None,
):
    """
    Keyword arguments:

    signup -- Indicates whether or not sending the
    email is essential (during signup), or if it can be skipped (e.g. in
    case email verification is optional and we are only logging in).
    """
    # Local users are stopped due to form validation checking
    # is_active, yet, adapter methods could toy with is_active in a
    # `user_signed_up` signal. Furthermore, social users should be
    # stopped anyway.
    adapter = get_adapter(request)
    if not user.is_active:
        return adapter.respond_user_inactive(request, user)

    if email_verification == app_settings.EmailVerificationMethod.NONE:
        pass
    elif email_verification == app_settings.EmailVerificationMethod.OPTIONAL:
        # In case of OPTIONAL verification: send on signup.
        if not _has_verified_for_login(user, email) and signup:
            send_email_confirmation(request, user, signup=signup, email=email)
    elif email_verification == app_settings.EmailVerificationMethod.MANDATORY:
        if not _has_verified_for_login(user, email):
            send_email_confirmation(request, user, signup=signup, email=email)
            return adapter.respond_email_verification_sent(request, user)
    try:
        adapter.login(request, user)
        response = HttpResponseRedirect(
            get_login_redirect_url(request, redirect_url, signup=signup)
        )

        if signal_kwargs is None:
            signal_kwargs = {}
        signals.user_logged_in.send(
            sender=user.__class__,
            request=request,
            response=response,
            user=user,
            **signal_kwargs,
        )
        adapter.add_message(
            request,
            messages.SUCCESS,
            "account/messages/logged_in.txt",
            {"user": user},
        )
    except ImmediateHttpResponse as e:
        response = e.response
    return response


def complete_signup(request, user, email_verification, success_url, signal_kwargs=None):
    if signal_kwargs is None:
        signal_kwargs = {}
    signals.user_signed_up.send(
        sender=user.__class__, request=request, user=user, **signal_kwargs
    )
    return perform_login(
        request,
        user,
        email_verification=email_verification,
        signup=True,
        redirect_url=success_url,
        signal_kwargs=signal_kwargs,
    )


def cleanup_email_addresses(request, addresses):
    """
    Takes a list of EmailAddress instances and cleans it up, making
    sure only valid ones remain, without multiple primaries etc.

    Order is important: e.g. if multiple primary e-mail addresses
    exist, the first one encountered will be kept as primary.
    """
    from .models import EmailAddress

    adapter = get_adapter(request)
    # Let's group by `email`
    e2a = OrderedDict()  # maps email to EmailAddress
    primary_addresses = []
    verified_addresses = []
    primary_verified_addresses = []
    for address in addresses:
        # Pick up only valid ones...
        email = valid_email_or_none(address.email)
        if not email:
            continue
        # ... and non-conflicting ones...
        if (
            app_settings.UNIQUE_EMAIL
            and EmailAddress.objects.filter(email__iexact=email).exists()
        ):
            continue
        a = e2a.get(email.lower())
        if a:
            a.primary = a.primary or address.primary
            a.verified = a.verified or address.verified
        else:
            a = address
            a.verified = a.verified or adapter.is_email_verified(request, a.email)
            e2a[email.lower()] = a
        if a.primary:
            primary_addresses.append(a)
            if a.verified:
                primary_verified_addresses.append(a)
        if a.verified:
            verified_addresses.append(a)
    # Now that we got things sorted out, let's assign a primary
    if primary_verified_addresses:
        primary_address = primary_verified_addresses[0]
    elif verified_addresses:
        # Pick any verified as primary
        primary_address = verified_addresses[0]
    elif primary_addresses:
        # Okay, let's pick primary then, even if unverified
        primary_address = primary_addresses[0]
    elif e2a:
        # Pick the first
        primary_address = e2a.keys()[0]
    else:
        # Empty
        primary_address = None
    # There can only be one primary
    for a in e2a.values():
        a.primary = primary_address.email.lower() == a.email.lower()
    return list(e2a.values()), primary_address


def setup_user_email(request, user, addresses):
    """
    Creates proper EmailAddress for the user that was just signed
    up. Only sets up, doesn't do any other handling such as sending
    out email confirmation mails etc.
    """
    from .models import EmailAddress

    assert not EmailAddress.objects.filter(user=user).exists()
    priority_addresses = []
    # Is there a stashed e-mail?
    adapter = get_adapter(request)
    stashed_email = adapter.unstash_verified_email(request)
    if stashed_email:
        priority_addresses.append(
            EmailAddress(user=user, email=stashed_email, primary=True, verified=True)
        )
    email = user_email(user)
    if email:
        priority_addresses.append(
            EmailAddress(user=user, email=email, primary=True, verified=False)
        )
    addresses, primary = cleanup_email_addresses(
        request, priority_addresses + addresses
    )
    for a in addresses:
        a.user = user
        a.save()
    EmailAddress.objects.fill_cache_for_user(user, addresses)
    if primary and email and email.lower() != primary.email.lower():
        user_email(user, primary.email)
        user.save()
    return primary


def send_email_confirmation(request, user, signup=False, email=None):
    """
    E-mail verification mails are sent:
    a) Explicitly: when a user signs up
    b) Implicitly: when a user attempts to log in using an unverified
    e-mail while EMAIL_VERIFICATION is mandatory.

    Especially in case of b), we want to limit the number of mails
    sent (consider a user retrying a few times), which is why there is
    a cooldown period before sending a new mail. This cooldown period
    can be configured in ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN setting.
    """
    from .models import EmailAddress, EmailConfirmation

    cooldown_period = timedelta(seconds=app_settings.EMAIL_CONFIRMATION_COOLDOWN)

    if not email:
        email = user_email(user)
    if email:
        try:
            email_address = EmailAddress.objects.get_for_user(user, email)
            if not email_address.verified:
                if app_settings.EMAIL_CONFIRMATION_HMAC:
                    send_email = True
                else:
                    send_email = not EmailConfirmation.objects.filter(
                        sent__gt=now() - cooldown_period,
                        email_address=email_address,
                    ).exists()
                if send_email:
                    email_address.send_confirmation(request, signup=signup)
            else:
                send_email = False
        except EmailAddress.DoesNotExist:
            send_email = True
            email_address = EmailAddress.objects.add_email(
                request, user, email, signup=signup, confirm=True
            )
            assert email_address
        # At this point, if we were supposed to send an email we have sent it.
        if send_email:
            get_adapter(request).add_message(
                request,
                messages.INFO,
                "account/messages/" "email_confirmation_sent.txt",
                {"email": email},
            )
    if signup:
        get_adapter(request).stash_user(request, user_pk_to_url_str(user))


def sync_user_email_addresses(user):
    """
    Keep user.email in sync with user.emailaddress_set.

    Under some circumstances the user.email may not have ended up as
    an EmailAddress record, e.g. in the case of manually created admin
    users.
    """
    from .models import EmailAddress

    email = user_email(user)
    if (
        email
        and not EmailAddress.objects.filter(user=user, email__iexact=email).exists()
    ):
        if (
            app_settings.UNIQUE_EMAIL
            and EmailAddress.objects.filter(email__iexact=email).exists()
        ):
            # Bail out
            return
        EmailAddress.objects.create(
            user=user, email=email, primary=False, verified=False
        )


def filter_users_by_username(*username):
    if app_settings.PRESERVE_USERNAME_CASING:
        qlist = [
            Q(**{app_settings.USER_MODEL_USERNAME_FIELD + "__iexact": u})
            for u in username
        ]
        q = qlist[0]
        for q2 in qlist[1:]:
            q = q | q2
        ret = get_user_model().objects.filter(q)
    else:
        ret = get_user_model().objects.filter(
            **{
                app_settings.USER_MODEL_USERNAME_FIELD
                + "__in": [u.lower() for u in username]
            }
        )
    return ret


def filter_users_by_email(email, is_active=None):
    """Return list of users by email address

    Typically one, at most just a few in length.  First we look through
    EmailAddress table, than customisable User model table. Add results
    together avoiding SQL joins and deduplicate.
    """
    from .models import EmailAddress

    User = get_user_model()
    mails = EmailAddress.objects.filter(email__iexact=email)
    if is_active is not None:
        mails = mails.filter(user__is_active=is_active)
    users = []
    for e in mails.prefetch_related("user"):
        if _unicode_ci_compare(e.email, email):
            users.append(e.user)
    if app_settings.USER_MODEL_EMAIL_FIELD:
        q_dict = {app_settings.USER_MODEL_EMAIL_FIELD + "__iexact": email}
        user_qs = User.objects.filter(**q_dict)
        if is_active is not None:
            user_qs = user_qs.filter(is_active=is_active)
        for user in user_qs.iterator():
            user_email = getattr(user, app_settings.USER_MODEL_EMAIL_FIELD)
            if _unicode_ci_compare(user_email, email):
                users.append(user)
    return list(set(users))


def passthrough_next_redirect_url(request, url, redirect_field_name):
    assert url.find("?") < 0  # TODO: Handle this case properly
    next_url = get_next_redirect_url(request, redirect_field_name)
    if next_url:
        url = url + "?" + urlencode({redirect_field_name: next_url})
    return url


def user_pk_to_url_str(user):
    """
    This should return a string.
    """
    User = get_user_model()
    if issubclass(type(User._meta.pk), models.UUIDField):
        if isinstance(user.pk, str):
            return user.pk
        return user.pk.hex

    ret = user.pk
    if isinstance(ret, int):
        ret = int_to_base36(user.pk)
    return str(ret)


def url_str_to_user_pk(s):
    User = get_user_model()
    # TODO: Ugh, isn't there a cleaner way to determine whether or not
    # the PK is a str-like field?
    if getattr(User._meta.pk, "remote_field", None):
        pk_field = User._meta.pk.remote_field.to._meta.pk
    else:
        pk_field = User._meta.pk
    if issubclass(type(pk_field), models.UUIDField):
        return pk_field.to_python(s)
    try:
        pk_field.to_python("a")
        pk = s
    except ValidationError:
        pk = base36_to_int(s)
    return pk


# Magic number 7: if you run into collisions with this number, then you are
# of big enough scale to start investing in a decent user model...
MAX_USERNAME_SUFFIX_LENGTH = 7
USERNAME_SUFFIX_CHARS = [string.digits] * 4 + [string.ascii_letters] * (
    MAX_USERNAME_SUFFIX_LENGTH - 4
)


def _generate_unique_username_base(txts, regex=None):
    from FunctionModule.accounts.adapter import get_adapter

    adapter = get_adapter()
    username = None
    regex = regex or r"[^\w\s@+.-]"
    for txt in txts:
        if not txt:
            continue
        username = unicodedata.normalize("NFKD", force_str(txt))
        username = username.encode("ascii", "ignore").decode("ascii")
        username = force_str(re.sub(regex, "", username).lower())
        # Django allows for '@' in usernames in order to accomodate for
        # project wanting to use e-mail for username. In allauth we don't
        # use this, we already have a proper place for putting e-mail
        # addresses (EmailAddress), so let's not use the full e-mail
        # address and only take the part leading up to the '@'.
        username = username.split("@")[0]
        username = username.strip()
        username = re.sub(r"\s+", "_", username)
        # Finally, validating base username without database lookups etc.
        try:
            username = adapter.clean_username(username, shallow=True)
            break
        except ValidationError:
            pass
    return username or "user"


def get_username_max_length():

    if app_settings.USER_MODEL_USERNAME_FIELD is not None:
        User = get_user_model()
        max_length = User._meta.get_field(app_settings.USER_MODEL_USERNAME_FIELD).max_length
    else:
        max_length = 0
    return max_length


def generate_username_candidate(basename, suffix_length):
    max_length = get_username_max_length()
    suffix = "".join(
        random.choice(USERNAME_SUFFIX_CHARS[i]) for i in range(suffix_length)
    )
    return basename[0 : max_length - len(suffix)] + suffix


def generate_username_candidates(basename):
    if len(basename) >= app_settings.USERNAME_MIN_LENGTH:
        ret = [basename]
    else:
        ret = []
    min_suffix_length = max(1, app_settings.USERNAME_MIN_LENGTH - len(basename))
    max_suffix_length = min(get_username_max_length(), MAX_USERNAME_SUFFIX_LENGTH)
    for suffix_length in range(min_suffix_length, max_suffix_length):
        ret.append(generate_username_candidate(basename, suffix_length))
    return ret


def generate_unique_username(txts, regex=None):
    from FunctionModule.accounts.utils import filter_users_by_username

    from FunctionModule.accounts.adapter import get_adapter

    adapter = get_adapter()
    basename = _generate_unique_username_base(txts, regex)
    candidates = generate_username_candidates(basename)
    existing_usernames = filter_users_by_username(*candidates).values_list(
        app_settings.USER_MODEL_USERNAME_FIELD, flat=True
    )
    existing_usernames = set([n.lower() for n in existing_usernames])
    for candidate in candidates:
        if candidate.lower() not in existing_usernames:
            try:
                return adapter.clean_username(candidate, shallow=True)
            except ValidationError:
                pass
    # This really should not happen
    raise NotImplementedError("Unable to find a unique username")


def valid_email_or_none(email):
    ret = None
    try:
        if email:
            validate_email(email)
            if len(email) <= EmailField().max_length:
                ret = email
    except ValidationError:
        pass
    return ret


def email_address_exists(email, exclude_user=None):
    from FunctionModule.accounts import app_settings as account_settings
    from FunctionModule.accounts.models import EmailAddress

    emailaddresses = EmailAddress.objects
    if exclude_user:
        emailaddresses = emailaddresses.exclude(user=exclude_user)
    ret = emailaddresses.filter(email__iexact=email).exists()
    if not ret:
        email_field = account_settings.USER_MODEL_EMAIL_FIELD
        if email_field:
            users = get_user_model().objects
            if exclude_user:
                users = users.exclude(pk=exclude_user.pk)
            ret = users.filter(**{email_field + "__iexact": email}).exists()
    return ret
