from typing import Set

import django.contrib.admin.sites
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import Group

from .forms import MyUserChangeForm, GroupAdminForm
from .models import User

# Unregister the original Group admin.
try:
    admin.site.unregister(Group)
except django.contrib.admin.sites.NotRegistered:
    pass


class AccountAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    fieldsets = (('User Profile', {'fields': (
        'is_realtor', 'first_time', 'phone',
        'address', 'dob', 'gender',
        'bio', 'website', 'facebook', 'youtube',)}),
                 ) + AuthUserAdmin.fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'name', 'email', 'date_joined', 'phone', 'is_realtor')
    list_display_links = ('id', 'email')
    search_fields = ['email', 'phone']
    list_filter = (
        'date_joined', 'is_realtor', 'is_superuser', 'is_staff'
    )
    readonly_fields = [
        'date_joined',
    ]

    # change_list_template = 'admin/auth/user/change_list.html'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions'
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

    # def get_urls(self):
    #     urls = super(AccountAdmin, self).get_urls()
    #     custom_urls = []
    #     custom_urls = [
    #         url(
    #             r'^change/$',
    #             self.admin_site.admin_view(self.changelist_view),
    #             name='user-change',
    #         ),
    #         url(
    #             r'^delete/$',
    #             self.admin_site.admin_view(self.delete_view),
    #             name='user-delete',
    #         ),
    #     ]
    #     print urls
    #     print custom_urls
    #     return custom_urls + urls


class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    filter_horizontal = ['permissions']

admin.site.register(Group, GroupAdmin)
admin.site.register(User, AccountAdmin)
