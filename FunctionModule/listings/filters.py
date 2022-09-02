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

    list_date = NumberFilter(field_name='list_date', lookup_expr='year')
    list_date__gt = NumberFilter(field_name='list_date', lookup_expr='year__gt')
    list_date__lt = NumberFilter(field_name='list_date', lookup_expr='year__lt')

    class Meta:
        model = Listing
        fields = {
            'price': ['lt', 'gt'],
            'list_date': ['exact', 'year__gt'],
        }
