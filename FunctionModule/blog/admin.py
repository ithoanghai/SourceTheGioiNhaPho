# -*- coding: utf-8 -*-
from django.http import HttpRequest

from FunctionModule import admin_site
from FunctionModule.blog.forms import PostAdminForm
from FunctionModule.blog.models import Post


class PostAdmin(admin_site.ModelAdmin):
    form = PostAdminForm

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


admin_site.site.register(Post, PostAdmin)
