from django.db import models
from django.utils.translation import gettext as _


class CustomerStatus(models.TextChoices):
    NEW = 'new', _("Mới đi xem nhà")
    NEED = 'need', _("Cần mua gấp")
    SEE_MORE = 'see_more', _("Xem đã nhiều nhưng chưa ưng BĐS nào")
    MISSED_PURCHASE = 'missed_purchase', _("Đã từng chốt hụt")


class CustomerClassify(models.TextChoices):
    FOCUSED_CARE = 'focused_care', _("Cần chăm tập trung")
    NORMAL_CARE = 'normal_care', _("Chăm bình thường")
    SLOWLY_CARE = 'slowly_care', _("Chăm từ từ")
    STOP_CARE = 'stop_care', _("Dừng chăm sóc")
    AGAIN_CARE = 'again_care', _("Chăm sóc lại")
