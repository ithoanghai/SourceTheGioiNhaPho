from django import template

from FunctionModule.cadastral.constants import all_districts, state_data

register = template.Library()


@register.simple_tag
def get_district(district_code):
    try:
        district = all_districts.get(district_code)
        return district['name']
    except KeyError:
        return district_code


@register.simple_tag
def get_state(state_code):
    try:
        state = state_data.get(state_code)
        return state['name']
    except KeyError:
        return state_code
