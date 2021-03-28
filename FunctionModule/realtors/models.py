from datetime import datetime

from django.db import models

from FunctionModule.accounts.models import User


class Realtor(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    is_mvp = models.BooleanField(default=False)
    hire_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.user)
