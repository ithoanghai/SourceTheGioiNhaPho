from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomSocialAccountConfig(AppConfig):
    name = "FunctionModule.social_account"
    verbose_name = _("Tài khoản mạng xã hội")