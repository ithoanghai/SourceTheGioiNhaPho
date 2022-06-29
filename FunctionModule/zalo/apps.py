from django.apps import AppConfig


class ZaloConfig(AppConfig):
    name = 'FunctionModule.zalo'
    verbose_name = "Mạng XH Zalo"

    def ready(self):
        pass