from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'FunctionModule.blog'
    verbose_name = "Bài viết"

    def ready(self):
        pass