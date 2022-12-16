from django import template

from FunctionModule.listings import get_short_title_from_house_type, get_short_title_from_road_type, \
    get_listing_status_title_from_code, get_short_title_from_transaction_type, get_menu_from_choices, \
    get_short_title_from_direction, get_short_title_from_registration_type
from FunctionModule.listings.models import Listing
from FunctionModule.transactions.helpers import get_short_title_from_trans_type, get_short_title_from_customer_type, \
    get_short_title_from_position_type, get_short_title_type
from TownhouseWorldRealestate import settings

register = template.Library()


@register.filter(name='location_image')
def tag_get_listing_location_image(value):
    img_path = f'photos/listings/{value}/locations/static.png'
    # path = os.path.join(settings.MEDIA_ROOT, img_path)
    # if os.path.isfile(path):
    #     return TextNode(settings.MEDIA_URL + img_path)
    return settings.MEDIA_URL + img_path


@register.filter(name='get_road_type')
def tag_get_road_type(road_type):
    return get_short_title_from_road_type(road_type)


@register.filter(name='get_house_type')
def tag_get_house_type(house_type):
    return get_short_title_from_house_type(house_type)


@register.filter(name='get_transaction_type')
def tag_get_transaction_type(transaction_type):
    return get_short_title_from_transaction_type(transaction_type)


@register.filter(name='get_listing_status')
def tag_get_listing_status(listing_status):
    return get_listing_status_title_from_code(listing_status)


@register.filter(name='default_img_by_house_type')
def tag_get_default_img(house_type):
    return f'/static/img/default_house_type/{house_type}.jpg'


@register.filter(name='get_trans_type')
def tag_get_house_type(trans_type):
    return get_short_title_from_trans_type(trans_type)


@register.filter(name='get_customs_type')
def tag_get_customer_type(customs_type):
    return get_short_title_from_customer_type(customs_type)


@register.filter(name='get_menu_choices')
def tag_get_menu_choices():
    return get_menu_from_choices()


@register.filter(name='get_position_type')
def tag_get_position_type(position_type):
    return get_short_title_from_position_type(position_type)


@register.filter(name='get_title_type')
def tag_get_title_type(title_type):
    return get_short_title_type(title_type)


@register.filter(name='get_listing_count')
def tag_get_listing_count():
    return Listing.objects.all().count()


@register.filter(name='get_direction')
def tag_get_direction(direction):
    return get_short_title_from_direction(direction)


@register.filter(name='get_registration_type')
def tag_get_registration_type(registration_type):
    return get_short_title_from_registration_type(registration_type)