from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'FunctionModule.accounts'

    def ready(self):
        import FunctionModule.accounts.signals  # noqa