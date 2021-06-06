from datetime import datetime

from django.db import models


class Contact(models.Model):
    listing = models.CharField(max_length=200)
    listing_id = models.IntegerField()
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(default=datetime.now, blank=True)
    user_id = models.IntegerField(blank=True)
    is_processed = models.BooleanField(default=False)
    session_key = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'{self.name} - {self.phone}'


class RequestQuote(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    user_id = models.IntegerField(blank=True)
    house_type = models.CharField(max_length=20, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    request_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_processed = models.BooleanField(default=False)
    session_key = models.CharField(max_length=256, blank=True)
    contact_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f'{self.name} - {self.phone}'
