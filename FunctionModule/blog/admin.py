# -*- coding: utf-8 -*-
from FunctionModule import admin_site
from FunctionModule.blog.models import Post

admin_site.site.register(Post)
