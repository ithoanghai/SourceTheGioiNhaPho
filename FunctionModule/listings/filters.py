from __future__ import absolute_import

try:
    from django_filters import BaseInFilter
    _df_version = 2
except ImportError:
    from django_filters.fields import Lookup
    _df_version = 1.1


from django_filters import FilterSet, CharFilter, BooleanFilter, DateFilter, NumberFilter

from FunctionModule.listings.models import Listing

if _df_version >= 2:
    class MultipleCharFilter(BaseInFilter, CharFilter):
        pass

class ListingFilter(FilterSet):
    realtor = CharFilter(field_name='realtor', lookup_expr='iexact')
    transaction_type = MultipleCharFilter(field_name='transaction_type')

    class Meta:
        model = Listing
        fields = ['realtor', 'transaction_type', 'registration_type']


