from django import template
from django.conf import settings

from FunctionModule.listings import get_short_title_from_house_type, get_short_title_from_road_type

register = template.Library()


@register.filter(name='location_image')
def tag_get_listing_location_image(value):
    img_path = f'photos/listings/{value}/locations/static.png'
    # path = os.path.join(settings.MEDIA_ROOT, img_path)
    # if os.path.isfile(path):
    #     return TextNode(settings.MEDIA_URL + img_path)
    return settings.MEDIA_URL + img_path


@register.filter(name='get_house_type')
def tag_get_house_type(house_type):
    return get_short_title_from_house_type(house_type)


@register.filter(name='get_road_type')
def tag_get_road_type(road_type):
    return get_short_title_from_road_type(road_type)


@register.filter(name='default_img_by_house_type')
def tag_get_default_img(house_type):
    return f'/static/img/default_house_type/{house_type}.jpg'
