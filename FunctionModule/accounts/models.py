from __future__ import absolute_import
from datetime import datetime
from django.core import signing
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser, GroupManager, UserManager, PermissionManager, \
    _user_has_module_perms, _user_get_permissions, _user_has_perm
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import get_random_string
from django.utils.encoding import force_str

import FunctionModule
from .constants import GENDER_CHOICES
from . import app_settings, signals, providers
from .managers import EmailAddressManager, EmailConfirmationManager
from .utils import get_next_redirect_url, setup_user_email, user_email
from .adapter import get_adapter
from TownhouseWorldRealestate.utils import get_user_model, get_request_param
from TownhouseWorldRealestate.settings import AUTH_USER_MODEL

from .fields import JSONField


def default_hire_date():
    return timezone.now()


phone_regex = RegexValidator(regex=r'^(09|03|07|08|05)+([0-9]{8})$',
                             message="Số điện thoại 10 số với chỉ các đầu số 09|03|07|08|05")


class Permission(models.Model):
    """
    The permissions system provides a way to assign permissions to specific
    users and groups of users.

    The permission system is used by the Django admin site, but may also be
    useful in your own code. The Django admin site uses permissions as follows:

        - The "add" permission limits the user's ability to view the "add" form
          and add an object.
        - The "change" permission limits a user's ability to view the change
          list, view the "change" form and change an object.
        - The "delete" permission limits the ability to delete an object.
        - The "view" permission limits the ability to view an object.

    Permissions are set globally per type of object, not per specific object
    instance. It is possible to say "Mary may change news stories," but it's
    not currently possible to say "Mary may change news stories, but only the
    ones she created herself" or "Mary may only change news stories that have a
    certain status or publication date."

    The permissions listed above are automatically created for each model.
    """
    name = models.CharField(_('Tên quyền'), max_length=255)
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        verbose_name=_('Chức năng'),
        related_name='django'
    )
    codename = models.CharField(_('Mã chức năng'), max_length=100)

    objects = PermissionManager()

    class Meta:
        verbose_name = _('Quyền sử dụng')
        verbose_name_plural = _('DS Quyền sử dụng')
        unique_together = [['content_type', 'codename']]
        ordering = ['content_type__app_label', 'content_type__model', 'codename']

    def __str__(self):
        return '%s | %s' % (self.content_type, self.name)

    def natural_key(self):
        return (self.codename,) + self.content_type.natural_key()
    natural_key.dependencies = ['contenttypes.contenttype']


class Group(models.Model):
    """
    Overwrites original Django Group.
    """
    class Meta:
        verbose_name = "Nhóm người dùng"
        verbose_name_plural = "DS Nhóm người dùng"

    name = models.CharField(_('Tên nhóm'), max_length=150, unique=True)
    permissions = models.ManyToManyField(
        to='accounts.Permission',
        verbose_name=_('Quyền sử dụng'),
        blank=True,
        related_name='Group'
    )

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class PermissionsMixin(models.Model):
    """
    Add the fields and methods necessary to support the Group and Permission
    models using the ModelBackend.
    """
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('Nhóm người dùng'),
        blank=True,
        help_text=_(
            'Nhóm quyền mà người dùng này được phân quyền.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('Quyền người dùng'),
        blank=True,
        help_text=_('Xác định quyền cho người dùng này.'),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True


class User(AbstractUser, PermissionsMixin):
    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "DS Người dùng"
        ordering = ["first_name", "last_name"]

    # These two fields are for backend (admin) login form to display correctly
    username = models.CharField(
        _('Tên đăng nhập'), max_length=150, unique=True,
        help_text=_(
            'Bắt buộc nhập. Không quá 150 ký tự. Có thể bao gồm ký tự, chữ số và chỉ ký tự đặc biệt @/./+/-/_.'),
        error_messages={'unique': _("Người dùng này đã tồn tại trên hệ thống.")},
    )
    email = models.EmailField(_('Email'), blank=True, unique=True, error_messages={
        'unique': _("Email này đã được sử dụng trên hệ thống.")})

    # Basic Info
    first_name = models.CharField(_('Họ Đệm'), max_length=150, blank=True)
    last_name = models.CharField(_('Tên'), max_length=150, blank=True)
    phone = models.CharField(_('Điện thoại'), max_length=20, db_index=True, unique=True,
                             validators=[phone_regex],
                             error_messages={'unique': _("Số điện thoại này đã được sử dụng trên hệ thống.")})
    address = models.CharField(_('Địa chỉ nơi ở'), blank=True, max_length=255)
    dob = models.DateField(_('Ngày sinh'), blank=True, null=True)
    gender = models.CharField(_('Giới tính'), max_length=20, choices=GENDER_CHOICES, blank=True,
                              default='male')
    bio = models.TextField(_('Giới thiệu bản thân'), blank=True)
    avatar = models.ImageField(_("Ảnh đại diện"), upload_to="photos/%Y%m%d/", blank=True)

    is_broker = models.BooleanField(default=False, verbose_name=_("MUỐN LÀM MÔI GIỚI"))
    is_investor = models.BooleanField(default=False, verbose_name=_("MUỐN LÀM ĐẦU TƯ"))
    is_active = models.BooleanField(default=True, verbose_name=_("ĐÃ KÍCH HOẠT"))
    is_staff = models.BooleanField(default=False, verbose_name=_("LÀ CHUYÊN VIÊN TGNP"))
    is_superuser = models.BooleanField(default=False, verbose_name=_("LÀ QUẢN TRỊ HỆ THỐNG"))
    # Metadata
    first_time = models.BooleanField(_('Đăng nhập lần đầu'), default=True)
    date_joined = models.DateField(_('Ngày gia nhập'), default=timezone.now, blank=True, null=True)
    last_login = models.DateTimeField(_('Đăng nhập lần cuối'), default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f'%s - %s' % (self.name, self.phone)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    @property
    def name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username

    def user_image(self):
        return '<img src="%s"/>' % self.avatar

    user_image.allow_tags = True


class Point(models.Model):
    class Meta:
        verbose_name = "Điểm số"
        verbose_name_plural = "Điểm đạt được"

    user = models.OneToOneField(User, on_delete=models.RESTRICT, db_constraint=User, blank=True, null=True)
    investment_point = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)], verbose_name=_("Điểm đầu tư"), null=True, blank=True, default=0)
    investment_account = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999999)],
                                           verbose_name=_("Tài khoản có đầu tư (Triệu đồng)"), null=True, blank=True, default=0)
    prestige_points = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)], verbose_name=_("Điểm uy tín"), null=True, blank=True, default=0)
    potential_points = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)], verbose_name=_("Điểm tiềm năng"), null=True, blank=True, default=0)
    bds_referral_point = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)], verbose_name=_("Điểm giới thiệu BĐS"), null=True, blank=True,default=0)
    customer_referral_point = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)], verbose_name=_("Điểm giới thiệu khách"), null=True, blank=True,default=0)

    def __str__(self):
        return f'%s' % (self.user)


class EmailAddress(models.Model):

    user = models.ForeignKey(AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
    )
    email = models.EmailField(
        unique=app_settings.UNIQUE_EMAIL,
        max_length=app_settings.EMAIL_MAX_LENGTH,
        verbose_name=_("e-mail address"),
    )
    verified = models.BooleanField(verbose_name=_("verified"), default=False)
    primary = models.BooleanField(verbose_name=_("primary"), default=False)

    objects = EmailAddressManager()

    class Meta:
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")
        if not app_settings.UNIQUE_EMAIL:
            unique_together = [("user", "email")]

    def __str__(self):
        return self.email

    def set_as_primary(self, conditional=False):
        old_primary = EmailAddress.objects.get_primary(self.user)
        if old_primary:
            if conditional:
                return False
            old_primary.primary = False
            old_primary.save()
        self.primary = True
        self.save()
        user_email(self.user, self.email)
        self.user.save()
        return True

    def send_confirmation(self, request=None, signup=False):
        if app_settings.EMAIL_CONFIRMATION_HMAC:
            confirmation = EmailConfirmationHMAC(self)
        else:
            confirmation = EmailConfirmation.create(self)
        confirmation.send(request, signup=signup)
        return confirmation

    def change(self, request, new_email, confirm=True):
        """
        Given a new email address, change self and re-confirm.
        """
        with transaction.atomic():
            user_email(self.user, new_email)
            self.user.save()
            self.email = new_email
            self.verified = False
            self.save()
            if confirm:
                self.send_confirmation(request)


class EmailConfirmation(models.Model):

    email_address = models.ForeignKey(
        EmailAddress,
        verbose_name=_("e-mail address"),
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(verbose_name=_("created"), default=timezone.now)
    sent = models.DateTimeField(verbose_name=_("sent"), null=True)
    key = models.CharField(verbose_name=_("key"), max_length=64, unique=True)

    objects = EmailConfirmationManager()

    class Meta:
        verbose_name = _("email confirmation")
        verbose_name_plural = _("email confirmations")

    def __str__(self):
        return "confirmation for %s" % self.email_address

    @classmethod
    def create(cls, email_address):
        key = get_random_string(64).lower()
        return cls._default_manager.create(email_address=email_address, key=key)

    def key_expired(self):
        expiration_date = self.sent + datetime.timedelta(
            days=app_settings.EMAIL_CONFIRMATION_EXPIRE_DAYS
        )
        return expiration_date <= timezone.now()

    key_expired.boolean = True

    def confirm(self, request):
        if not self.key_expired() and not self.email_address.verified:
            email_address = self.email_address
            get_adapter(request).confirm_email(request, email_address)
            signals.email_confirmed.send(
                sender=self.__class__,
                request=request,
                email_address=email_address,
            )
            return email_address

    def send(self, request=None, signup=False):
        get_adapter(request).send_confirmation_mail(request, self, signup)
        self.sent = timezone.now()
        self.save()
        signals.email_confirmation_sent.send(
            sender=self.__class__,
            request=request,
            confirmation=self,
            signup=signup,
        )


class EmailConfirmationHMAC:
    def __init__(self, email_address):
        self.email_address = email_address

    @property
    def key(self):
        return signing.dumps(obj=self.email_address.pk, salt=app_settings.SALT)

    @classmethod
    def from_key(cls, key):
        try:
            max_age = 60 * 60 * 24 * app_settings.EMAIL_CONFIRMATION_EXPIRE_DAYS
            pk = signing.loads(key, max_age=max_age, salt=app_settings.SALT)
            ret = EmailConfirmationHMAC(EmailAddress.objects.get(pk=pk))
        except (
            signing.SignatureExpired,
            signing.BadSignature,
            EmailAddress.DoesNotExist,
        ):
            ret = None
        return ret

    def confirm(self, request):
        if not self.email_address.verified:
            email_address = self.email_address
            get_adapter(request).confirm_email(request, email_address)
            signals.email_confirmed.send(
                sender=self.__class__,
                request=request,
                email_address=email_address,
            )
            return email_address

    def send(self, request=None, signup=False):
        get_adapter(request).send_confirmation_mail(request, self, signup)
        signals.email_confirmation_sent.send(
            sender=self.__class__,
            request=request,
            confirmation=self,
            signup=signup,
        )


class SocialAppManager(models.Manager):
    def get_current(self, provider, request=None):
        cache = {}
        if request:
            cache = getattr(request, "_socialapp_cache", {})
            request._socialapp_cache = cache
        app = cache.get(provider)
        if not app:
            site = get_current_site(request)
            app = self.get(sites__id=site.id, provider=provider)
            cache[provider] = app
        return app


class SocialApp(models.Model):
    objects = SocialAppManager()

    provider = models.CharField(
        verbose_name=_("provider"),
        max_length=30,
        choices=providers.registry.as_choices(),
    )
    name = models.CharField(verbose_name=_("name"), max_length=40)
    client_id = models.CharField(
        verbose_name=_("client id"),
        max_length=191,
        help_text=_("App ID, or consumer key"),
    )
    secret = models.CharField(
        verbose_name=_("secret key"),
        max_length=191,
        blank=True,
        help_text=_("API secret, client secret, or" " consumer secret"),
    )
    key = models.CharField(
        verbose_name=_("key"), max_length=191, blank=True, help_text=_("Key")
    )
    # Most apps can be used across multiple domains, therefore we use
    # a ManyToManyField. Note that Facebook requires an app per domain
    # (unless the domains share a common base name).
    # blank=True allows for disabling apps without removing them
    sites = models.ManyToManyField(Site, blank=True)

    # We want to move away from storing secrets in the database. So, we're
    # putting a halt towards adding more fields for additional secrets, such as
    # the certificate some providers need. Therefore, the certificate is not a
    # DB backed field and can only be set using the ``APP`` configuration key
    # in the provider settings.
    certificate_key = None

    class Meta:
        verbose_name = _("social application")
        verbose_name_plural = _("social applications")

    def __str__(self):
        return self.name


class SocialAccount(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.CharField(
        verbose_name=_("provider"),
        max_length=30,
        choices=providers.registry.as_choices(),
    )
    # Just in case you're wondering if an OpenID identity URL is going
    # to fit in a 'uid':
    #
    # Ideally, URLField(max_length=1024, unique=True) would be used
    # for identity.  However, MySQL has a max_length limitation of 191
    # for URLField (in case of utf8mb4). How about
    # models.TextField(unique=True) then?  Well, that won't work
    # either for MySQL due to another bug[1]. So the only way out
    # would be to drop the unique constraint, or switch to shorter
    # identity URLs. Opted for the latter, as [2] suggests that
    # identity URLs are supposed to be short anyway, at least for the
    # old spec.
    #
    # [1] http://code.djangoproject.com/ticket/2495.
    # [2] http://openid.net/specs/openid-authentication-1_1.html#limits

    uid = models.CharField(
        verbose_name=_("uid"), max_length=app_settings.UID_MAX_LENGTH
    )
    last_login = models.DateTimeField(verbose_name=_("last login"), auto_now=True)
    date_joined = models.DateTimeField(verbose_name=_("date joined"), auto_now_add=True)
    extra_data = JSONField(verbose_name=_("extra data"), default=dict)

    class Meta:
        unique_together = ("provider", "uid")
        verbose_name = _("social account")
        verbose_name_plural = _("social accounts")

    def authenticate(self):
        return authenticate(account=self)

    def __str__(self):
        return force_str(self.user)

    def get_profile_url(self):
        return self.get_provider_account().get_profile_url()

    def get_avatar_url(self):
        return self.get_provider_account().get_avatar_url()

    def get_provider(self):
        return providers.registry.by_id(self.provider)

    def get_provider_account(self):
        return self.get_provider().wrap_account(self)


class SocialToken(models.Model):
    app = models.ForeignKey(SocialApp, on_delete=models.CASCADE)
    account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE)
    token = models.TextField(
        verbose_name=_("token"),
        help_text=_('"oauth_token" (OAuth1) or access token (OAuth2)'),
    )
    token_secret = models.TextField(
        blank=True,
        verbose_name=_("token secret"),
        help_text=_('"oauth_token_secret" (OAuth1) or refresh token (OAuth2)'),
    )
    expires_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_("expires at")
    )

    class Meta:
        unique_together = ("app", "account")
        verbose_name = _("social application token")
        verbose_name_plural = _("social application tokens")

    def __str__(self):
        return self.token


class SocialLogin(object):
    """
    Represents a social user that is in the process of being logged
    in. This consists of the following information:

    `account` (`SocialAccount` instance): The social account being
    logged in. Providers are not responsible for checking whether or
    not an account already exists or not. Therefore, a provider
    typically creates a new (unsaved) `SocialAccount` instance. The
    `User` instance pointed to by the account (`account.user`) may be
    prefilled by the provider for use as a starting point later on
    during the signup process.

    `token` (`SocialToken` instance): An optional access token token
    that results from performing a successful authentication
    handshake.

    `state` (`dict`): The state to be preserved during the
    authentication handshake. Note that this state may end up in the
    url -- do not put any secrets in here. It currently only contains
    the url to redirect to after login.

    `email_addresses` (list of `EmailAddress`): Optional list of
    e-mail addresses retrieved from the provider.
    """

    def __init__(self, user=None, account=None, token=None, email_addresses=[]):
        if token:
            assert token.account is None or token.account == account
        self.token = token
        self.user = user
        self.account = account
        self.email_addresses = email_addresses
        self.state = {}

    def connect(self, request, user):
        self.user = user
        self.save(request, connect=True)

    def serialize(self):
        serialize_instance = get_adapter().serialize_instance
        ret = dict(
            account=serialize_instance(self.account),
            user=serialize_instance(self.user),
            state=self.state,
            email_addresses=[serialize_instance(ea) for ea in self.email_addresses],
        )
        if self.token:
            ret["token"] = serialize_instance(self.token)
        return ret

    @classmethod
    def deserialize(cls, data):
        deserialize_instance = get_adapter().deserialize_instance
        account = deserialize_instance(SocialAccount, data["account"])
        user = deserialize_instance(get_user_model(), data["user"])
        if "token" in data:
            token = deserialize_instance(SocialToken, data["token"])
        else:
            token = None
        email_addresses = []
        for ea in data["email_addresses"]:
            email_address = deserialize_instance(EmailAddress, ea)
            email_addresses.append(email_address)
        ret = cls()
        ret.token = token
        ret.account = account
        ret.user = user
        ret.email_addresses = email_addresses
        ret.state = data["state"]
        return ret

    def save(self, request, connect=False):
        """
        Saves a new account. Note that while the account is new,
        the user may be an existing one (when connecting accounts)
        """
        assert not self.is_existing
        user = self.user
        user.save()
        self.account.user = user
        self.account.save()
        if app_settings.STORE_TOKENS and self.token and self.token.app_id:
            self.token.account = self.account
            self.token.save()
        if connect:
            # TODO: Add any new email addresses automatically?
            pass
        else:
            setup_user_email(request, user, self.email_addresses)

    @property
    def is_existing(self):
        """
        Account is temporary, not yet backed by a database record.
        """
        return self.account.pk is not None

    def lookup(self):
        """
        Lookup existing account, if any.
        """
        assert not self.is_existing
        try:
            a = SocialAccount.objects.get(
                provider=self.account.provider, uid=self.account.uid
            )
            # Update account
            a.extra_data = self.account.extra_data
            self.account = a
            self.user = self.account.user
            a.save()
            # Update token
            if app_settings.STORE_TOKENS and self.token and self.token.app.pk:
                assert not self.token.pk
                try:
                    t = SocialToken.objects.get(
                        account=self.account, app=self.token.app
                    )
                    t.token = self.token.token
                    if self.token.token_secret:
                        # only update the refresh token if we got one
                        # many oauth2 providers do not resend the refresh token
                        t.token_secret = self.token.token_secret
                    t.expires_at = self.token.expires_at
                    t.save()
                    self.token = t
                except SocialToken.DoesNotExist:
                    self.token.account = a
                    self.token.save()
        except SocialAccount.DoesNotExist:
            pass

    def get_redirect_url(self, request):
        url = self.state.get("next")
        return url

    @classmethod
    def state_from_request(cls, request):
        state = {}
        next_url = get_next_redirect_url(request)
        if next_url:
            state["next"] = next_url
        state["process"] = get_request_param(request, "process", "login")
        state["scope"] = get_request_param(request, "scope", "")
        state["auth_params"] = get_request_param(request, "auth_params", "")
        return state

    @classmethod
    def stash_state(cls, request):
        state = cls.state_from_request(request)
        verifier = get_random_string(12)
        request.session["socialaccount_state"] = (state, verifier)
        return verifier

    @classmethod
    def unstash_state(cls, request):
        if "socialaccount_state" not in request.session:
            raise PermissionDenied()
        state, verifier = request.session.pop("socialaccount_state")
        return state

    @classmethod
    def verify_and_unstash_state(cls, request, verifier):
        if "socialaccount_state" not in request.session:
            raise PermissionDenied()
        state, verifier2 = request.session.pop("socialaccount_state")
        if verifier != verifier2:
            raise PermissionDenied()
        return state
