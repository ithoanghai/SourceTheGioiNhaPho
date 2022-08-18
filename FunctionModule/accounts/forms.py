from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserChangeForm
from django.forms import Textarea, TextInput, EmailInput
from .models import User, phone_regex, Group


class MyUserChangeForm(UserChangeForm):
    dob = forms.DateField(label='Ngày sinh', help_text='ngày-tháng-năm', widget=forms.DateInput(format='%d-%m-%Y'), input_formats=['%d-%m-%Y'], required=False)

    class Meta(UserChangeForm.Meta):
        model = User

        widgets = {
            'bio': Textarea(attrs={'class': '???', 'rows': 3}),
        }


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
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


from django import forms

from allauth.account.forms import SignupForm


class CustomUserCreationForm(SignupForm):

    email = forms.IntegerField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    def save(self, request):

        user = super(CustomUserCreationForm, self).save(request)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        # You must return the original result.
        return user