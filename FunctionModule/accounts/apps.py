from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'FunctionModule.accounts'
    verbose_name = "Người dùng hệ thống"

    def ready(self):
        import FunctionModule.accounts.signals  # noqa


