# from FunctionModule.accounts.models import Point
# from TownhouseWorldRealestate.utils import phone_random
#
#
# @receiver(post_save, sender=Point)
# def point_add_handler(sender, instance: Point, **kwargs):
#      instance.user.save()
#
#
# @receiver(pre_delete, sender=Point)
# def point_delete_handler(sender, instance: Point, **kwargs):
#     instance.user.save()


# @receiver(user_signed_up)
# def user_signed_up_handler(request: WSGIRequest, user, **kwargs):
#     if 'facebook/login/callback' in request.path:
#         user.username = user.email
#         user.phone = phone_random(10)
#         user.save()
