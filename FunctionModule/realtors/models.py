from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from pkg_resources import require
from django.utils.translation import gettext as _
from FunctionModule.accounts.models import User
from FunctionModule.listings import HouseType
from FunctionModule.listings.choices import Position, Title


def default_hire_date():
    return timezone.now()


class Realtor(models.Model):
    class Meta:
        verbose_name = "Chuyên viên"
        verbose_name_plural = "DS Chuyên viên"

    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    name = models.CharField(max_length=50, verbose_name=_("Tên"), null=True, blank=True)
    position = models.CharField(max_length=20, choices=Position.choices, verbose_name=_("Chức danh"),default=Position.USER)
    title = models.CharField(max_length=20, choices=Title.choices, verbose_name=_("Danh hiệu"), default=Title.ROOKIE)
    level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], choices=([(i, i) for i in range(1, 10)]), default=1, verbose_name=_("Đẳng cấp chuyên môn"))
    work_area = models.CharField(max_length=100, verbose_name=_("Địa bàn khu vực Quận/Huyện hoạt động"), null=True, blank=True, default="Hoàng Mai")
    hire_date = models.DateTimeField(default=default_hire_date, blank=True)

    def __str__(self):
        return f'%s' % (self.user)
