from allauth.account.signals import user_signed_up
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import random

from FunctionModule.accounts.models import Point


@receiver(post_save, sender=Point)
def point_add_handler(sender, instance: Point, **kwargs):
     instance.user.save()


@receiver(pre_delete, sender=Point)
def point_delete_handler(sender, instance: Point, **kwargs):
    instance.user.save()


def phone_random(length):
    number = '0123456789'
    #alpha = 'abcdefghijklmnopqrstuvwxyz'
    id = '09'
    for i in range(0,length-2):
        id += random.choice(number)
        #id += random.choice(alpha)
    return id


@receiver(user_signed_up)
def user_signed_up_handler(request: WSGIRequest, user, **kwargs):
    if 'facebook/login/callback' in request.path:
        user.username = user.email
        user.phone = phone_random(10)
        user.save()
