from django.apps import AppConfig


class ListingsConfig(AppConfig):
    name = 'FunctionModule.listings'
    verbose_name = "Kho hàng BĐS"

    def ready(self):
        from allauth.account import signals
        pass
