from ajax_select import register, LookupChannel

from .constants import district_data, DISTRICT_LOOKUP_CHANNEL, WARD_LOOKUP_CHANNEL, ward_data


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
