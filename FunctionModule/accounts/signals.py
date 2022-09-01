from django.core.handlers.wsgi import WSGIRequest
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver, Signal
from django.contrib.auth.signals import user_logged_out  # noqa

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


# Provides the arguments "request", "user"
user_logged_in = Signal()

# Typically followed by `user_logged_in` (unless, e-mail verification kicks in)
# Provides the arguments "request", "user"
user_signed_up = Signal()

# Provides the arguments "request", "user"
password_set = Signal()
# Provides the arguments "request", "user"
password_changed = Signal()
# Provides the arguments "request", "user"
password_reset = Signal()

# Provides the arguments "request", "email_address"
email_confirmed = Signal()
# Provides the arguments "request", "confirmation", "signup"
email_confirmation_sent = Signal()

# Provides the arguments "request", "user", "from_email_address",
# "to_email_address"
email_changed = Signal()
# Provides the arguments "request", "user", "email_address"
email_added = Signal()
# Provides the arguments "request", "user", "email_address"
email_removed = Signal()


# Sent after a user successfully authenticates via a social provider,
# but before the login is actually processed. This signal is emitted
# for social logins, signups and when connecting additional social
# accounts to an account.
# Provides the arguments "request", "sociallogin"
pre_social_login = Signal()

# Sent after a user connects a social account to a their local account.
# Provides the arguments "request", "sociallogin"
social_account_added = Signal()

# Sent after a user connects an already existing social account to a
# their local account. The social account will have an updated token and
# refreshed extra_data.
# Provides the arguments "request", "sociallogin"
social_account_updated = Signal()

# Sent after a user disconnects a social account from their local
# account.
# Provides the arguments "request", "socialaccount"
social_account_removed = Signal()