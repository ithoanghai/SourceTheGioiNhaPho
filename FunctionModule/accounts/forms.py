from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from django.forms import Textarea, TextInput, EmailInput

from .models import User, phone_regex, CustomGroup


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

        widgets = {
            'bio': Textarea(attrs={'class': '???', 'rows': 3}),
        }


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = CustomGroup
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        # Use the pretty 'filter_horizontal widget'.
        widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super().__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super().save()
        # Save many-to-many data
        self.save_m2m()
        return instance


class UserRegisterForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'phone', 'email')
        # fields = UserChangeForm.Meta.fields #+ ("email",)
        field_order = ['first_name', 'last_name', ]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)


class UserProfileForm(UserChangeForm):
    avatar = forms.ImageField(required=False)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'phone', 'email', 'bio', 'gender', 'dob', 'address','website','facebook','youtube','avatar',)
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