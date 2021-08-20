from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.utils.translation import gettext as _

from FunctionModule.accounts.models import User
from FunctionModule.listings.choices import HouseType
from FunctionModule.listings.models import Listing
from FunctionModule.realtors.models import Realtor

class TransTypeInit(models.TextChoices):
    CONTACT = 'contact', _("Liên hệ")
    ORDER = 'oder', _("Đặt hàng")
    BUY = 'buy', _("Mua")
    SELL = 'sell', _("Bán")
    RENT = 'rent', _("Thuê")
    LEASE = 'lease', _("Cho thuê")
    INTRO_ESTATE = 'intro_estate', _("Giới thiệu BĐS")
    INTRO_CUSTO = 'intro_custo', _("Giới thiệu Khách")


class Status(models.TextChoices):
    ACTIVE = 'active', _("Đang giao dịch")
    PAUSE = 'pause', _("Tạm dừng")
    CANCEL = 'cancelTransaction', _("Huỷ")
    COMPLETED ='completed', _("Hoàn thành")


class Reason(models.TextChoices):
    FEEDBACK = 'feedback', _("Trả lời khách")
    MEET = 'meet', _("Dẫn khách")
    NEGOTIATE = 'negotiate', _("Đàm phán")
    DEPOSIT = 'deposit', _("Đặt cọc")
    CANCEL_DEPOSIT = 'cancelDeposit', _("Bỏ cọc")
    CONTRACT = 'contract', _("Ký hợp đồng")
    CANCEL_CONTRACT = 'cancelTransaction', _("Huỷ hợp đồng")
    COMPLETED = 'completed', _("Hoàn tất giao dịch")


class Transaction(models.Model):
    class Meta:
        verbose_name = "Giao dịch BĐS"
        verbose_name_plural = "DS Giao dịch"
        ordering = ['date']

    trantype = models.CharField(max_length=25, choices=TransTypeInit.choices, default=TransTypeInit.CONTACT, verbose_name='Loại giao dịch')
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name=_("Bất động sản"))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name=_("Khách hàng"))

    house_type = models.CharField(max_length=20, null=True, blank=True, choices=HouseType.choices, verbose_name=_("Loại BĐS quan tâm"))
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Khu vực quan tâm"))
    request_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name=_("Giá kỳ vọng"))
    message = models.TextField(blank=True, null=True, verbose_name="Thông điệp của khách hàng")
    comment = models.TextField(max_length=100, blank=True, null=True, verbose_name="Mô tả thêm")
    date = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Thời gian phát sinh giao dịch")
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.ACTIVE, verbose_name='Trạng thái giao dịch')
    realtor = models.ForeignKey(Realtor, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Giao Chuyên viên quản lý"))

    def __str__(self):
        return f'%s:  %s' % (self.trantype, self.message)
