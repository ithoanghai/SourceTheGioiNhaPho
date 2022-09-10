from django.db import models
from django.utils.translation import gettext as _

from FunctionModule.cadastral.constants import state_data, ward_data, all_districts, district_data


class PostType(models.TextChoices):
    MARKET = 'market', _("Thị trường")
    INVEST = 'invest', _("Đầu tư")
    ENTERPRISE = 'enterprise', _("Doanh nghiệp")
    IDENTIFY = 'identify', _("Chuyên gia trao đổi")
    ZONING = 'zoning', _("Quy hoạch")
    PROJECT = 'project', _("Dự án")
    UTILITY = 'utility', _("Dịch vụ & Tiện ích ")
    POLICY = 'policy', _("Chính sách & Pháp luật")
