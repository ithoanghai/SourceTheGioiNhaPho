import django_filters
from django_filters import FilterSet, CharFilter, BaseInFilter, RangeFilter
from django.contrib.admin.filters import (
    SimpleListFilter,
    AllValuesFieldListFilter,
    ChoicesFieldListFilter,
    RelatedFieldListFilter,
    RelatedOnlyFieldListFilter
)

from FunctionModule.listings.models import Listing


class MultipleCharFilter(BaseInFilter, CharFilter):
    pass


class ListingFilter(FilterSet):
    realtor = CharFilter(field_name='realtor', lookup_expr='iexact')
    transaction_type = MultipleCharFilter(field_name='transaction_type')

    class Meta:
        model = Listing
        fields = ['realtor', 'transaction_type', 'registration_type']


class AreaFilter(FilterSet):
    area = django_filters.AllValuesFilter()

    class Meta:
        model = Listing
        fields = ['area']


class IsWithinRangeFilter(SimpleListFilter):
    title = 'Title'
    parameter_name = 'scoreRange'
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        return queryset


class SimpleDropdownFilter(SimpleListFilter):
    template = 'admin/dropdown_filter.html'


class DropdownFilter(AllValuesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class ChoiceDropdownFilter(ChoicesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class RelatedDropdownFilter(RelatedFieldListFilter):
    template = 'admin/dropdown_filter.html'


class RelatedOnlyDropdownFilter(RelatedOnlyFieldListFilter):
    template = 'admin/dropdown_filter.html'