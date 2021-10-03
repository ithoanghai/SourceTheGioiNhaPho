import functools

from ajax_select import register, LookupChannel

from .constants import (DISTRICT_LOOKUP_CHANNEL, WARD_LOOKUP_CHANNEL, ward_data, state_data, district_data,
                        all_districts)


@register(DISTRICT_LOOKUP_CHANNEL)
class DistrictLookup(LookupChannel):

    def get_query(self, q, request):
        try:
            districts = district_data[q]
            return districts
        except Exception as e:
            print(e)
            return []

    def format_item_display(self, obj):
        return obj['name']

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


def get_wards_by_district(district):
    return ward_data[district]


@functools.cache
def get_ward(district, ward):
    ward = [x for x in get_wards_by_district(district) if x['code'] == ward]
    return ward[0]


@functools.cache
def get_ward_name(district, ward):
    try:
        ward = get_ward(district, ward)
        return ward['name']
    except (KeyError, IndexError):
        return ""


def get_state(code):
    return state_data[code]


def get_all_states():
    return state_data


@functools.cache
def get_all_districts():
    return all_districts


@functools.cache
def get_district(code):
    return all_districts[code]
