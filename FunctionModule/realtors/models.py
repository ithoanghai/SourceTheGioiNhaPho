from django.db import models
from django.utils import timezone

from FunctionModule.accounts.models import User


def default_hire_date():
    return timezone.now()


class Realtor(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    is_mvp = models.BooleanField(default=False)
    hire_date = models.DateTimeField(default=default_hire_date, blank=True)

    def __str__(self):
        return str(self.user)
