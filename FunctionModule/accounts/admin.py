from typing import Set

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialToken
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from .forms import MyUserChangeForm, GroupAdminForm
from .models import User


class AccountAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_fieldsets = (
        ('THÔNG TIN CƠ BẢN', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2',),
        }), ('THÔNG TIN BỔ SUNG', {'fields': (
            'first_time', 'first_name', 'last_name',
            'address', 'dob', 'gender',
            'avatar', 'facebook',)})
    )

    fieldsets = (
        ('THÔNG TIN CƠ BẢN', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password',)}),
        ('THÔNG TIN BỔ SUNG', {'fields': (
            'first_time', 'last_name', 'first_name',
            'address', 'dob', 'gender',
            'bio', 'avatar', 'user_image',  'website', 'facebook', 'youtube',)}),
        ('PHÂN QUYỀN SỬ DỤNG', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('THỜI GIAN HOẠT ĐỘNG', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('id', 'name', 'phone', 'email', 'date_joined', 'is_staff','user_image')
    list_display_links = ('name', 'email')
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']
    list_filter = ('date_joined', 'is_superuser', 'is_staff')
    list_per_page = 200
    readonly_fields = [
        'date_joined', 'user_image',
    ]
    ordering = ('username', 'last_name', 'id', 'date_joined',)

    # change_list_template = 'admin/auth/user/change_list.html'
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(id=request.user.id)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                'is_superuser',
                'user_permissions'
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    filter_horizontal = ['permissions']


admin.site.register(Group, GroupAdmin)
admin.site.register(User, AccountAdmin)
admin.site.unregister(TokenProxy)
admin.site.unregister(SocialToken)
admin.site.unregister(EmailAddress)
