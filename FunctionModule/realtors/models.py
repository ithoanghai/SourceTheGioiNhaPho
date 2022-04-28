from django.db import models
from django.utils import timezone

from FunctionModule.accounts.models import User


def default_hire_date():
    return timezone.now()


class Realtor(models.Model):
    class Meta:
        verbose_name = "Chuyên viên"
        verbose_name_plural = "DS Chuyên viên"

    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    #work_area = models.CharField(max_length=100, verbose_name=_("Địa bàn khu vực Quận/Huyện hoạt động"))
    hire_date = models.DateTimeField(default=default_hire_date, blank=True)

    def __str__(self):
        return f'%s' % (self.user)
