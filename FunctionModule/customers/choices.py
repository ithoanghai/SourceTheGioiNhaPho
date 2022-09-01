from django.db import models
from django.utils.translation import gettext as _


class CustomerType(models.TextChoices):
    BUY_LIVE = 'buy_to_live', _("Mua ở")
    KEEP_MONEY = 'keep_money', _("Đầu tư Giữ dòng tiền")
    REPAIR_CONSTRUCTION = 'repair_construction', _("Đầu tư sửa bán")
    INVESTMENT_CONSTRUCTION = 'invest_construction', _("Đầu tư xây bán")
    SURF_INVESTMENT = 'surf_investment', _("Đầu tư lướt sóng")
    RENT_LIVE = 'rent_to_live', _("Thuê ở")
    RENT_OFFICE = 'rent_to_office', _("Thuê làm văn phòng")
    RENT_RESTAURANT = 'rent_to_restaurant', _("Thuê làm nhà hàng")
    RENT_SHOP = 'rent_to_shop', _("Thuê làm cửa hàng")


class CustomerStatus(models.TextChoices):
    NEW = 'new', _("Mới đi xem nhà")
    SEE_MORE = 'see_more', _("Xem nhiều nhưng chưa ưng BĐS nào")
    HAVE_BUYING = 'have_buying', _("Đã từng mua/bán bđs")
    MISSED_PURCHASE = 'missed_purchase', _("Đã từng chốt hụt")


class CustomerClassify(models.TextChoices):
    FOCUSED_CARE = 'focused_care', _("Khách nét. Cần chăm tập trung")
    NORMAL_CARE = 'normal_care', _("Chăm bình thường")
    SLOWLY_CARE = 'slowly_care', _("Chăm từ từ")
    STOP_CARE = 'stop_care', _("Dừng chăm sóc")
    AGAIN_CARE = 'again_care', _("Chăm sóc lại")


class TransactionStatus(models.TextChoices):
    NEED = 'need', _("Cần mua/thuê gấp")
    NOT_YET = 'not_yet', _("Chưa mua/thuê")
    PAUSE_BUYING = 'pause_buying', _("Tạm dừng mua/thuê")
    BOUGHT = 'bought', _("Đã mua/thuê")
    STOP_BUYING = 'stop_buying', _("Dừng quan tâm")
