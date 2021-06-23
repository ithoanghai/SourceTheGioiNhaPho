from allauth.account.signals import user_signed_up
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from FunctionModule.realtors.models import Realtor


@receiver(post_save, sender=Realtor)
def realtor_add_handler(sender, instance: Realtor, **kwargs):
    instance.user.is_realtor = True
    instance.user.save()


@receiver(pre_delete, sender=Realtor)
def realtor_delete_handler(sender, instance: Realtor, **kwargs):
    instance.user.is_realtor = False
    instance.user.save()


@receiver(user_signed_up)
def user_signed_up_handler(request: WSGIRequest, user, **kwargs):
    if 'facebook/login/callback' in request.path:
        user.username = user.email
        user.save()
