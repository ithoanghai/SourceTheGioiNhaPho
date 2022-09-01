from typing import Set

from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin, GroupAdmin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db import transaction, router
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import escape
from django.utils.translation import gettext
from rest_framework.authtoken.models import TokenProxy
from django.utils.translation import ugettext_lazy as _

from .forms import MyUserChangeForm, GroupAdminForm
from .models import User, Groups, Permissions
from ..filters import DateFieldFilter, BooleanFieldFilter


class PermissionAdmin(admin.ModelAdmin):
    search_fields = ('name', 'content_type', 'codename')
    ordering = ('content_type','name')
    verbose_name = "Quản trị Quyền người dùng"


class AccountAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_fieldsets = (
        ('THÔNG TIN CƠ BẢN', {
            'classes': ('wide',),
            'fields': (('username','first_name', 'last_name'),('password1', 'password2'), ('phone','email')),
        }), ('THÔNG TIN BỔ SUNG', {'fields': (
            ('address', 'dob', 'gender'),
            ('avatar', 'bio',),
            ('is_broker', 'is_investor',))})
    )

    fieldsets = (
        ('THÔNG TIN CƠ BẢN', {
            'classes': ('wide',),
            'fields': (('username', 'password'), ('phone', 'email'))}),
        ('THÔNG TIN BỔ SUNG', {'fields': (
            ('first_name', 'last_name'),
            ('address', 'dob', 'gender'),
            'avatar', 'bio', ('is_broker', 'is_investor',))}),
        ('PHÂN QUYỀN SỬ DỤNG', {
            'fields': (('is_active', 'is_staff', 'is_superuser'), ('groups', 'permissions'))
        }),
        ('THỜI GIAN HOẠT ĐỘNG', {'fields': ('first_time', 'date_joined','last_login')}),
    )

    list_display = ('id', 'name', 'phone', 'email', 'date_joined', 'is_staff', 'is_broker', 'is_investor')
    list_display_links = ('name', 'phone')
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']
    list_filter = ('date_joined', 'is_broker', 'is_investor', 'is_staff', 'is_active')
    list_filter = (
        ('date_joined', DateFieldFilter),
        ('is_broker', BooleanFieldFilter),
        ('is_investor', BooleanFieldFilter),
        ('is_active', BooleanFieldFilter),
    )
    list_per_page = 200
    readonly_fields = [
        'date_joined', 'user_image',
    ]
    ordering = ('first_name', 'last_name', 'date_joined', )
    filter_horizontal = ('groups',)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    # change_list_template = 'admin/auth/user/change_list.html'
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(id=request.user.id)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)

        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                'is_superuser',
                'permissions'
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

    def user_change_password(self, request, id, form_url=''):
        user = self.get_object(request, unquote(id))
        if not self.has_change_permission(request, user):
            raise PermissionDenied
        if user is None:
            raise Http404(_('%(name)s người dùng này có khóa %(key)r không tồn tại.') % {
                'name': self.model._meta.verbose_name,
                'key': escape(id),
            })
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, user, change_message)
                msg = gettext('Mật khẩu thay đổi thành công.')
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(
                    reverse(
                        '%s:%s_%s_change' % (
                            self.admin_site.name,
                            user._meta.app_label,
                            user._meta.model_name,
                        ),
                        args=(user.pk,),
                    )
                )
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Thay đổi mật khẩu cho người dùng: %s') % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
            **self.admin_site.each_context(request),
        }

        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            self.change_user_password_template or
            'admin/auth/user/change_password.html',
            context,
        )


class GroupAdmin(GroupAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)
    verbose_name = "Quản trị nhóm người dùng"
    form = GroupAdminForm


admin.site.register(Permissions,PermissionAdmin)
#admin.site.register(ContentType)
admin.site.register(Groups, GroupAdmin)
admin.site.register(User, AccountAdmin)
admin.site.unregister(TokenProxy)
#admin.site.unregister(SocialToken)
#admin.site.unregister(EmailAddress)
