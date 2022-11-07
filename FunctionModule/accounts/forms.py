from __future__ import absolute_import
from django import forms
from django.core import exceptions, validators
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _, pgettext
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import UserChangeForm, UsernameField, ReadOnlyPasswordHashField
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.forms import Textarea, TextInput, EmailInput
from .models import User, phone_regex, Groups, SocialAccount

import warnings
from importlib import import_module

from TownhouseWorldRealestate.utils import (
    build_absolute_uri,
    set_form_field_order,
)
from . import app_settings, signals
from .adapter import get_adapter
from .models import EmailAddress
from .utils import (
    filter_users_by_email,
    get_username_max_length,
    get_user_model,
    perform_login,
    setup_user_email,
    sync_user_email_addresses,
    url_str_to_user_pk,
    user_email,
    user_pk_to_url_str,
    user_username,
)

UserModel = get_user_model()


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Groups
        exclude = []
        fields = ('name','permissions')


class UserRegisterForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'phone', 'email', 'is_broker', 'is_investor')
        # fields = UserChangeForm.Meta.fields #+ ("email",)
        field_order = ['first_name', 'last_name', ]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)


class UserProfileForm(UserChangeForm):
    avatar = forms.ImageField(required=False)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'phone', 'email', 'bio', 'gender', 'dob', 'address', 'avatar', 'is_broker', 'is_investor')
        # fields = UserChangeForm.Meta.fields #+ ("email",)
        field_order = ['first_name', 'last_name', ]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)


class EmailAwarePasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        ret = super(EmailAwarePasswordResetTokenGenerator, self)._make_hash_value(
            user, timestamp
        )
        sync_user_email_addresses(user)
        emails = set([user.email] if user.email else [])
        emails.update(
            EmailAddress.objects.filter(user=user).values_list("email", flat=True)
        )
        ret += "|".join(sorted(emails))
        return ret


default_token_generator = EmailAwarePasswordResetTokenGenerator()


class PasswordVerificationMixin(object):
    def clean(self):
        cleaned_data = super(PasswordVerificationMixin, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if (password1 and password2) and password1 != password2:
            self.add_error("password2", _("You must type the same password each time."))
        return cleaned_data


class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs):
        render_value = kwargs.pop(
            "render_value", app_settings.PASSWORD_INPUT_RENDER_VALUE
        )
        kwargs["widget"] = forms.PasswordInput(
            render_value=render_value,
            attrs={"placeholder": kwargs.get("label")},
        )
        autocomplete = kwargs.pop("autocomplete", None)
        if autocomplete is not None:
            kwargs["widget"].attrs["autocomplete"] = autocomplete
        super(PasswordField, self).__init__(*args, **kwargs)


class SetPasswordField(PasswordField):
    def __init__(self, *args, **kwargs):
        kwargs["autocomplete"] = "new-password"
        super(SetPasswordField, self).__init__(*args, **kwargs)
        self.user = None

    def clean(self, value):
        value = super(SetPasswordField, self).clean(value)
        value = get_adapter().clean_password(value, user=self.user)
        return value


class LoginForm(forms.Form):

    password = PasswordField(label=_("Mật khẩu"), autocomplete="current-password")
    remember = forms.BooleanField(label=_("Ghi nhó mật khẩu"), required=False)

    user = None
    error_messages = {
        "account_inactive": _("This account is currently inactive."),
        "email_password_mismatch": _(
            "The e-mail address and/or password you specified are not correct."
        ),
        "username_password_mismatch": _(
            "The username and/or password you specified are not correct."
        ),
    }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)
        if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
            login_widget = forms.TextInput(
                attrs={
                    "type": "email",
                    "placeholder": _("E-mail address"),
                    "autocomplete": "email",
                }
            )
            login_field = forms.EmailField(label=_("E-mail"), widget=login_widget)
        elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
            login_widget = forms.TextInput(
                attrs={"placeholder": _("Tên đăng nhập"), "autocomplete": "username"}
            )
            login_field = forms.CharField(
                label=_("Username"),
                widget=login_widget,
                max_length=get_username_max_length(),
            )
        else:
            assert (
                app_settings.AUTHENTICATION_METHOD
                == app_settings.AuthenticationMethod.USERNAME_EMAIL
            )
            login_widget = forms.TextInput(
                attrs={"placeholder": _("Tên đăng nhập hoặc e-mail"), "autocomplete": "email"}
            )
            login_field = forms.CharField(
                label=pgettext("field label", "Đăng nhập"), widget=login_widget
            )
        self.fields["login"] = login_field
        set_form_field_order(self, ["login", "password", "remember"])
        if app_settings.SESSION_REMEMBER is not None:
            del self.fields["remember"]

    def user_credentials(self):
        """
        Provides the credentials required to authenticate the user for
        login.
        """
        credentials = {}
        login = self.cleaned_data["login"]
        if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
            credentials["email"] = login
        elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
            credentials["username"] = login
        else:
            if self._is_login_email(login):
                credentials["email"] = login
            credentials["username"] = login
        credentials["password"] = self.cleaned_data["password"]
        return credentials

    def clean_login(self):
        login = self.cleaned_data["login"]
        return login.strip()

    def _is_login_email(self, login):
        try:
            validators.validate_email(login)
            ret = True
        except exceptions.ValidationError:
            ret = False
        return ret

    def clean(self):
        super(LoginForm, self).clean()
        if self._errors:
            return
        credentials = self.user_credentials()
        user = get_adapter(self.request).authenticate(self.request, **credentials)
        if user:
            self.user = user
        else:
            auth_method = app_settings.AUTHENTICATION_METHOD
            if auth_method == app_settings.AuthenticationMethod.USERNAME_EMAIL:
                login = self.cleaned_data["login"]
                if self._is_login_email(login):
                    auth_method = app_settings.AuthenticationMethod.EMAIL
                else:
                    auth_method = app_settings.AuthenticationMethod.USERNAME
            raise forms.ValidationError(
                self.error_messages["%s_password_mismatch" % auth_method]
            )
        return self.cleaned_data

    def login(self, request, redirect_url=None):
        email = self.user_credentials().get("email")
        ret = perform_login(
            request,
            self.user,
            email_verification=app_settings.EMAIL_VERIFICATION,
            redirect_url=redirect_url,
            email=email,
        )
        remember = app_settings.SESSION_REMEMBER
        if remember is None:
            remember = self.cleaned_data["remember"]
        if remember:
            request.session.set_expiry(app_settings.SESSION_COOKIE_AGE)
        else:
            request.session.set_expiry(0)
        return ret


class _DummyCustomSignupForm(forms.Form):
    def signup(self, request, user):
        """
        Invoked at signup time to complete the signup of the user.
        """
        pass


def _base_signup_form_class():
    """
    Currently, we inherit from the custom form, if any. This is all
    not very elegant, though it serves a purpose:

    - There are two signup forms: one for local accounts, and one for
      social accounts
    - Both share a common base (BaseSignupForm)

    - Given the above, how to put in a custom signup form? Which form
      would your custom form derive from, the local or the social one?
    """
    if not app_settings.SIGNUP_FORM_CLASS:
        return _DummyCustomSignupForm
    try:
        fc_module, fc_classname = app_settings.SIGNUP_FORM_CLASS.rsplit(".", 1)
    except ValueError:
        raise exceptions.ImproperlyConfigured(
            "%s does not point to a form" " class" % app_settings.SIGNUP_FORM_CLASS
        )
    try:
        mod = import_module(fc_module)
    except ImportError as e:
        raise exceptions.ImproperlyConfigured(
            "Error importing form class %s:" ' "%s"' % (fc_module, e)
        )
    try:
        fc_class = getattr(mod, fc_classname)
    except AttributeError:
        raise exceptions.ImproperlyConfigured(
            'Module "%s" does not define a' ' "%s" class' % (fc_module, fc_classname)
        )
    if not hasattr(fc_class, "signup"):
        if hasattr(fc_class, "save"):
            warnings.warn(
                "The custom signup form must offer"
                " a `def signup(self, request, user)` method",
                DeprecationWarning,
            )
        else:
            raise exceptions.ImproperlyConfigured(
                'The custom signup form must implement a "signup" method'
            )
    return fc_class


class BaseSignupForm(_base_signup_form_class()):
    username = forms.CharField(
        label=_("Username"),
        min_length=app_settings.USERNAME_MIN_LENGTH,
        widget=forms.TextInput(
            attrs={"placeholder": _("Username"), "autocomplete": "username"}
        ),
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "placeholder": _("E-mail address"),
                "autocomplete": "email",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        email_required = kwargs.pop("email_required", app_settings.EMAIL_REQUIRED)
        self.username_required = kwargs.pop(
            "username_required", app_settings.USERNAME_REQUIRED
        )
        super(BaseSignupForm, self).__init__(*args, **kwargs)
        username_field = self.fields["username"]
        username_field.max_length = get_username_max_length()
        username_field.validators.append(
            validators.MaxLengthValidator(username_field.max_length)
        )
        username_field.widget.attrs["maxlength"] = str(username_field.max_length)

        default_field_order = [
            "email",
            "email2",  # ignored when not present
            "username",
            "password1",
            "password2",  # ignored when not present
        ]
        if app_settings.SIGNUP_EMAIL_ENTER_TWICE:
            self.fields["email2"] = forms.EmailField(
                label=_("E-mail (again)"),
                widget=forms.TextInput(
                    attrs={
                        "type": "email",
                        "placeholder": _("E-mail address confirmation"),
                    }
                ),
            )
        if email_required:
            self.fields["email"].label = gettext("E-mail")
            self.fields["email"].required = True
        else:
            self.fields["email"].label = gettext("E-mail (optional)")
            self.fields["email"].required = False
            self.fields["email"].widget.is_required = False
            if self.username_required:
                default_field_order = [
                    "username",
                    "email",
                    "email2",  # ignored when not present
                    "password1",
                    "password2",  # ignored when not present
                ]

        if not self.username_required:
            del self.fields["username"]

        set_form_field_order(
            self, getattr(self, "field_order", None) or default_field_order
        )

    def clean_username(self):
        value = self.cleaned_data["username"]
        value = get_adapter().clean_username(value)
        return value

    def clean_email(self):
        value = self.cleaned_data["email"]
        value = get_adapter().clean_email(value)
        if value and app_settings.UNIQUE_EMAIL:
            value = self.validate_unique_email(value)
        return value

    def validate_unique_email(self, value):
        return get_adapter().validate_unique_email(value)

    def clean(self):
        cleaned_data = super(BaseSignupForm, self).clean()
        if app_settings.SIGNUP_EMAIL_ENTER_TWICE:
            email = cleaned_data.get("email")
            email2 = cleaned_data.get("email2")
            if (email and email2) and email != email2:
                self.add_error("email2", _("You must type the same email each time."))
        return cleaned_data

    def custom_signup(self, request, user):
        custom_form = super(BaseSignupForm, self)
        if hasattr(custom_form, "signup") and callable(custom_form.signup):
            custom_form.signup(request, user)
        else:
            warnings.warn(
                "The custom signup form must offer"
                " a `def signup(self, request, user)` method",
                DeprecationWarning,
            )
            # Historically, it was called .save, but this is confusing
            # in case of ModelForm
            custom_form.save(user)


class SignupForm(BaseSignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["password1"] = PasswordField(
            label=_("Password"), autocomplete="new-password"
        )
        if app_settings.SIGNUP_PASSWORD_ENTER_TWICE:
            self.fields["password2"] = PasswordField(label=_("Password (again)"))

        if hasattr(self, "field_order"):
            set_form_field_order(self, self.field_order)

    def clean(self):
        super(SignupForm, self).clean()

        # `password` cannot be of type `SetPasswordField`, as we don't
        # have a `User` yet. So, let's populate a dummy user to be used
        # for password validaton.
        dummy_user = get_user_model()
        user_username(dummy_user, self.cleaned_data.get("username"))
        user_email(dummy_user, self.cleaned_data.get("email"))
        password = self.cleaned_data.get("password1")
        if password:
            try:
                get_adapter().clean_password(password, user=dummy_user)
            except forms.ValidationError as e:
                self.add_error("password1", e)

        if (
            app_settings.SIGNUP_PASSWORD_ENTER_TWICE
            and "password1" in self.cleaned_data
            and "password2" in self.cleaned_data
        ):
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                self.add_error(
                    "password2",
                    _("You must type the same password each time."),
                )
        return self.cleaned_data

    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        return user


class SignupFormSocial(BaseSignupForm):
    def __init__(self, *args, **kwargs):
        self.sociallogin = kwargs.pop("sociallogin")
        initial = get_adapter().get_signup_form_initial_data(self.sociallogin)
        kwargs.update(
            {
                "initial": initial,
                "email_required": kwargs.get(
                    "email_required", app_settings.EMAIL_REQUIRED
                ),
            }
        )
        super(SignupFormSocial, self).__init__(*args, **kwargs)

    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.save_user(request, self.sociallogin, form=self)
        self.custom_signup(request, user)
        return user

    def validate_unique_email(self, value):
        try:
            return super(SignupFormSocial, self).validate_unique_email(value)
        except forms.ValidationError:
            raise forms.ValidationError(
                get_adapter().error_messages["email_taken"]
                % self.sociallogin.account.get_provider().name
            )


class DisconnectForm(forms.Form):
    account = forms.ModelChoiceField(
        queryset=SocialAccount.objects.none(),
        widget=forms.RadioSelect,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.accounts = SocialAccount.objects.filter(user=self.request.user)
        super(DisconnectForm, self).__init__(*args, **kwargs)
        self.fields["account"].queryset = self.accounts

    def clean(self):
        cleaned_data = super(DisconnectForm, self).clean()
        account = cleaned_data.get("account")
        if account:
            get_adapter(self.request).validate_disconnect(account, self.accounts)
        return cleaned_data

    def save(self):
        account = self.cleaned_data["account"]
        account.delete()
        signals.social_account_removed.send(
            sender=SocialAccount, request=self.request, socialaccount=account
        )


class UserForm(forms.Form):
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)


class AddEmailForm(UserForm):

    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
        widget=forms.TextInput(
            attrs={"type": "email", "placeholder": _("E-mail address")}
        ),
    )

    def clean_email(self):
        value = self.cleaned_data["email"]
        value = get_adapter().clean_email(value)
        errors = {
            "this_account": _(
                "This e-mail address is already associated" " with this account."
            ),
            "different_account": _(
                "This e-mail address is already associated" " with another account."
            ),
            "max_email_addresses": _("You cannot add more than %d e-mail addresses."),
        }
        users = filter_users_by_email(value)
        on_this_account = [u for u in users if u.pk == self.user.pk]
        on_diff_account = [u for u in users if u.pk != self.user.pk]

        if on_this_account:
            raise forms.ValidationError(errors["this_account"])
        if on_diff_account and app_settings.UNIQUE_EMAIL:
            raise forms.ValidationError(errors["different_account"])
        if not EmailAddress.objects.can_add_email(self.user):
            raise forms.ValidationError(
                errors["max_email_addresses"] % app_settings.MAX_EMAIL_ADDRESSES
            )
        return value

    def save(self, request):
        return EmailAddress.objects.add_email(
            request, self.user, self.cleaned_data["email"], confirm=True
        )


class UserChangeForm(UserChangeForm):
    dob = forms.DateField(label='Ngày sinh', help_text='gõ theo định dạng: ngày-tháng-năm', widget=forms.DateInput(format='%d-%m-%Y'),
                          input_formats=['%d-%m-%Y'], required=False)
    password = ReadOnlyPasswordHashField(
        label=_("Mật khẩu"),
        help_text=_(
            'Mật khẩu đã mã hóa không được lưu trữ, không thể xem mật khẩu này '
            'nhưng có thể thay đổi mật khẩu bằng cách nhấp chọn  '
            '<a href="{}">Thay mật khẩu</a>.'
        ),
    )

    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': UsernameField}

        widgets = {
            'bio': Textarea(attrs={'class': '???', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get('password')


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields['username'].max_length = username_max_length
        self.fields['username'].widget.attrs['maxlength'] = username_max_length
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )


class ChangePasswordForm(PasswordVerificationMixin, UserForm):

    oldpassword = PasswordField(
        label=_("Mật khẩu hiện tại"), autocomplete="current-password"
    )
    password1 = SetPasswordField(label=_("Mật khẩu mới"))
    password2 = PasswordField(label=_("Gõ lại mật khẩu mới"))

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields["password1"].user = self.user

    def clean_oldpassword(self):
        if not self.user.check_password(self.cleaned_data.get("oldpassword")):
            raise forms.ValidationError(_("Hãy nhập mật khẩu hiện tại" " password."))
        return self.cleaned_data["oldpassword"]

    def save(self):
        get_adapter().set_password(self.user, self.cleaned_data["password1"])


class SetPasswordForm(PasswordVerificationMixin, UserForm):

    password1 = SetPasswordField(label=_("Mật khẩu mới"))
    password2 = PasswordField(label=_("Mật khẩu mới (Nhập lại)"))

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields["password1"].user = self.user

    def save(self):
        get_adapter().set_password(self.user, self.cleaned_data["password1"])


class ResetPasswordForm(forms.Form):

    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "placeholder": _("E-mail address"),
                "autocomplete": "email",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email, is_active=True)
        if not self.users:
            raise forms.ValidationError(
                _("The e-mail address is not assigned" " to any user account")
            )
        return self.cleaned_data["email"]

    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator", default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            path = reverse(
                "account_reset_password_from_key",
                kwargs=dict(uidb36=user_pk_to_url_str(user), key=temp_key),
            )
            url = build_absolute_uri(request, path)

            context = {
                "current_site": current_site,
                "user": user,
                "password_reset_url": url,
                "request": request,
            }

            if app_settings.AUTHENTICATION_METHOD != app_settings.AuthenticationMethod.EMAIL:
                context["username"] = user_username(user)
            get_adapter(request).send_mail(
                "account/email/password_reset_key", email, context
            )
        return self.cleaned_data["email"]


class ResetPasswordKeyForm(PasswordVerificationMixin, forms.Form):

    password1 = SetPasswordField(label=_("New Password"))
    password2 = PasswordField(label=_("New Password (again)"))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.temp_key = kwargs.pop("temp_key", None)
        super(ResetPasswordKeyForm, self).__init__(*args, **kwargs)
        self.fields["password1"].user = self.user

    def save(self):
        get_adapter().set_password(self.user, self.cleaned_data["password1"])


class UserTokenForm(forms.Form):

    uidb36 = forms.CharField()
    key = forms.CharField()

    reset_user = None
    token_generator = default_token_generator

    error_messages = {
        "token_invalid": _("The password reset token was invalid."),
    }

    def _get_user(self, uidb36):
        User = get_user_model()
        try:
            pk = url_str_to_user_pk(uidb36)
            return User.objects.get(pk=pk)
        except (ValueError, User.DoesNotExist):
            return None

    def clean(self):
        cleaned_data = super(UserTokenForm, self).clean()

        uidb36 = cleaned_data.get("uidb36", None)
        key = cleaned_data.get("key", None)

        if not key:
            raise forms.ValidationError(self.error_messages["token_invalid"])

        self.reset_user = self._get_user(uidb36)
        if self.reset_user is None or not self.token_generator.check_token(
            self.reset_user, key
        ):
            raise forms.ValidationError(self.error_messages["token_invalid"])

        return cleaned_data


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _('Hai trường mật khẩu không khớp.'),
    }
    password1 = forms.CharField(
        label=_("Mật khẩu"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Xác nhận mật khẩu"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Nhập mật khẩu lại, để xác nhận."),
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AdminAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app.
    """
    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': _(
            "Please enter the correct %(username)s and password for a staff "
            "account. Note that both fields may be case-sensitive."
        ),
    }
    required_css_class = 'required'

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
            )


class AdminPasswordChangeForm(ChangePasswordForm):
    required_css_class = 'required'