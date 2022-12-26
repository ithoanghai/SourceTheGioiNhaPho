from __future__ import absolute_import
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm, UsernameField, ReadOnlyPasswordHashField
from django.forms import Textarea
from .models import User, phone_regex
from allauth.account.utils import (
    get_user_model,
)

UserModel = get_user_model()


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

