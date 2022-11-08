# -*- coding: utf-8 -*-
from django.http import HttpRequest
from django.utils.translation import gettext as _, gettext_lazy
from FunctionModule import admin_site
from FunctionModule.admin_site import DateFieldListFilter
from FunctionModule.blog.forms import PostAdminForm
from FunctionModule.blog.models import Post


class PostAdmin(admin_site.ModelAdmin):
    fieldsets = (
        ('NỘI DUNG TIN ĐĂNG', {
            'classes': ('wide',),
            'fields': ('post_type', 'title', 'content')}),
        ('TÌNH TRẠNG TIN ĐĂNG', {'fields':
            ('user', ('is_published', 'date_update'))}),
    )

    form = PostAdminForm
    list_display = ('title', 'is_published', 'created_date','update_date',  'user')
    list_display_links = ('title',)
    list_filter = (
        ('date_created', DateFieldListFilter),
        ('date_update', DateFieldListFilter),
    )
    list_editable = ()
    search_fields = ('id', 'title', 'content', 'date_created', 'date_update')
    autocomplete_fields = ['user']
    list_per_page = 100
    inlines = []
    actions = ['make_published', 'unpublished',]
    ordering = ('-date_update',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(PostAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        disabled_fields = set()  # type: Set[str]
        disabled_fields |= {
            'user',
        }
        excludes = ('reward_person_mobile', 'extra_data')
        if request.user.is_superuser:
            form.base_fields['user'].disabled = True
        elif request.user.is_staff:
            for f in disabled_fields:
                if f in form.base_fields:
                    form.base_fields[f].disabled = True
        else:
            for f in disabled_fields:
                if f in form.base_fields:
                    form.base_fields[f].disabled = True
        return form

    def changeform_view(
        self,
        request: HttpRequest,
        object_id: int = None,
        form_url: str = '',
        extra_context: dict = None
    ) -> HttpRequest:

        extra_context = extra_context or {}
        extra_context.update({
            'show_save_as_copy': True,
        })
        return super().changeform_view(request, object_id, extra_context=extra_context)

    #@admin.actions(short_description='Đăng bán công khai')
    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'Đăng công khai {updated} tin bài')

    #@admin.actions(short_description='Không đăng bán')
    def unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'Chuyển riêng tư cho {updated} tin bài')


    make_published.short_description = _("Đăng công khai")
    unpublished.short_description = _("Hủy đăng công khai")

admin_site.site.register(Post, PostAdmin)
