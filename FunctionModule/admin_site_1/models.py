from django.utils.translation import gettext, gettext_lazy as _

ADDITION = 1
CHANGE = 2
DELETION = 3

ACTION_FLAG_CHOICES = (
    (ADDITION, _('Addition')),
    (CHANGE, _('Change')),
    (DELETION, _('Deletion')),
)

