from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from FunctionModule.accounts.models import User, phone_regex
from FunctionModule.realtors.models import Realtor


def default_hire_date():
    return timezone.now()


class Customer(models.Model):
    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "DS Khách hàng"

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.RESTRICT)
    name = models.CharField(_('Tên khách hàng'), null=True, blank=True, max_length=150)
    phone = models.CharField(_('Điện thoại'), max_length=20, db_index=True, unique=True, validators=[phone_regex],
                             error_messages={'unique': _("Số điện thoại này đã được sử dụng trên hệ thống.")})
    email = models.EmailField(_('Email'), null=True, blank=True, error_messages={
        'unique': _("Email này đã được sử dụng trên hệ thống.")})
    address = models.CharField(_('Địa chỉ'), blank=True, max_length=255)
    descriptions = models.TextField(_('Mô tả khách hàng'), blank=True)

    potential_points = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, default='0', verbose_name=_("Điểm tiềm năng"))
    realtor = models.ForeignKey(Realtor, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Chuyên viên phụ trách"))

    hire_date = models.DateTimeField(default=default_hire_date, blank=True)

    def __str__(self):
        return str(self.name)
