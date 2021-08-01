from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext as _

from FunctionModule.accounts.models import User
from FunctionModule.listings.models import Listing


class Status(models.TextChoices):
    FIND = 'find', _("Tìm kiếm")
    ORDER = 'oder', _("Đặt hàng")
    SAW = 'saw', _("Đã xem")
    NEGOTIATE = 'negotiate', _("Đàm phán")
    DEPOSIT = 'deposit', _("Đặt cọc")
    TRANSFER = 'transfer', _("Sang nhượng")
    CANCEL_DEPOSIT = 'cancelDeposit', _("Bỏ cọc")
    CANCEL_TRANSACTION = 'cancelTransaction', _("Huỷ giao dịch")


class Transaction(models.Model):
    class Meta:
        verbose_name_plural = "DS Giao dịch"

    code = models.CharField(max_length=13, help_text="Mã giao dịch")

    comment = models.TextField(help_text="Chú thích")

    price = models.FloatField(help_text="Giá")

    quantity = models.FloatField(help_text="Số lượng")

    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING, verbose_name=_("Bất động sản"))

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name=_("Khách hàng"))

    date = models.DateField(null=True, blank=True)

    reason = models.CharField(max_length=25, choices=Status.choices, blank=True, default=Status.FIND,
                              help_text='Lý do giao dịch')

    def __str__(self):
        return 'Transaction :  %s' % (self.comment)
