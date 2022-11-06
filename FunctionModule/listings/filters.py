from datetime import date

from FunctionModule.admin_site import SimpleListFilter
from django_filters import FilterSet, CharFilter, BaseInFilter, RangeFilter, NumberFilter

from FunctionModule.listings.models import Listing


class MultipleCharFilter(BaseInFilter, CharFilter):
    pass


class ListingFilter(FilterSet):
    price = NumberFilter()
    price__gt = NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = NumberFilter(field_name='price', lookup_expr='lt')

    date_update = NumberFilter(field_name='date_update', lookup_expr='year')
    date_update__gt = NumberFilter(field_name='date_update', lookup_expr='year__gt')
    date_update__lt = NumberFilter(field_name='date_update', lookup_expr='year__lt')

    class Meta:
        model = Listing
        fields = {
            'price': ['lt', 'gt'],
            'date_update': ['exact', 'year__gt'],
        }
