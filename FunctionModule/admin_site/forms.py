from django.forms import forms, Media

from FunctionModule.accounts.forms import AuthenticationForm, ChangePasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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


class RangeNumericForm(forms.Form):
    name = None

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        super().__init__(*args, **kwargs)

        self.fields[self.name + '_from'] = forms.FloatField(label='', required=False,
            widget=forms.NumberInput(attrs={'placeholder': _('From')}))
        self.fields[self.name + '_to'] = forms.FloatField(label='', required=False,
            widget=forms.NumberInput(attrs={'placeholder': _('To')}))

    @property
    def media(self):
        return super().media + Media(css=[self.NUMERIC_FILTER_CSS])


class SliderNumericForm(RangeNumericForm):
    pass