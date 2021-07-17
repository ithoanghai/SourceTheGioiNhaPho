import functools

from ajax_select import register, LookupChannel

from .constants import (DISTRICT_LOOKUP_CHANNEL, WARD_LOOKUP_CHANNEL, ward_data, state_data, district_data,
                        all_districts)


@register(DISTRICT_LOOKUP_CHANNEL)
class DistrictLookup(LookupChannel):

    def get_query(self, q, request):
        state_code = q
        try:
            districts = district_data[state_code]
            return districts
        except Exception as e:
            print(e)
            return []

    def format_item_display(self, item):
        return f"<option value='{item['code']}'>{item['name']}</option>"

    def get_result(self, obj):
        return obj['code']


@register(WARD_LOOKUP_CHANNEL)
class WardLookup(LookupChannel):

    def get_query(self, q, request):
        try:
            wards = ward_data[q]
            return wards
        except Exception as e:
            print(e)
            return []

    def format_item_display(self, obj):
        return obj['name']

    def get_result(self, obj):
        return obj['code']


@functools.cache
def get_state_name(code):
    try:
        return state_data[code]['name']
    except KeyError:
        return ""


@functools.cache
def get_district_name(code):
    try:
        return all_districts[code]['name']
    except KeyError:
        return ""


@functools.cache
def get_ward_name(district, ward):
    try:
        ward = [x for x in ward_data[district] if x['code'] == ward]
        return ward[0]['name']
    except (KeyError, IndexError):
        return ""


def get_all_states():
    return state_data

def get_default_districts():
    return district_data['01']