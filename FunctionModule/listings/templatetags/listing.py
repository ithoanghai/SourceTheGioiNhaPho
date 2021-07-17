import functools

from django import template
from django.conf import settings
from django.template.base import TextNode

register = template.Library()


def get_location_image(listing_id):
    img_path = f'photos/listings/{listing_id}/locations/static.png'
    # path = os.path.join(settings.MEDIA_ROOT, img_path)
    # if os.path.isfile(path):
    #     return TextNode(settings.MEDIA_URL + img_path)
    return settings.MEDIA_URL + img_path


@register.filter(name='location_image')
def tag_get_listing_location_image(value):
    return get_location_image(value)
