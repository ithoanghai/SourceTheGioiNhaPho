from datetime import date

from django.contrib.admin import SimpleListFilter
from django_filters import FilterSet, CharFilter, BaseInFilter, RangeFilter

from FunctionModule.filters import ChoicesFieldListFilter, BooleanFieldListFilter, DateFieldListFilter
from FunctionModule.listings.models import Listing


class MultipleCharFilter(BaseInFilter, CharFilter):
    pass


class ListingFilter(FilterSet):
    realtor = CharFilter(field_name='realtor', lookup_expr='iexact')
    transaction_type = MultipleCharFilter(field_name='transaction_type')

    class Meta:
        model = Listing
        fields = {
            'realtor': ['exact'],
            'transaction_type': ['exact'],
        }


class AreaFilter(SimpleListFilter):
    title = 'Diện tích:'
    parameter_name = 'scoreRange'
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        return (
            ('30', 'in the eighties'),
            ('50', 'in the nineties'),
        )

    def queryset(self, request, queryset):
        if self.value() == '30':
            return queryset.filter(
                area__gte=30,
                area__gte__lte=0,
            )
        if self.value() == '50':
            return queryset.filter(
                area__gte__gte=50,
                area__gte__lte=0,
            )


class IsWithinRangeFilter(SimpleListFilter):
    title = 'Lọc theo khoảng'
    parameter_name = 'scoreRange'
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        return (
            ('80s', 'in the eighties'),
            ('90s', 'in the nineties'),
        )

    def queryset(self, request, queryset):
        if self.value() == '80s':
            return queryset.filter(
                list_date__gte=date(1980, 1, 1),
                list_date__gte__lte=date(1989, 12, 31),
            )
        if self.value() == '90s':
            return queryset.filter(
                list_date__gte__gte=date(1990, 1, 1),
                list_date__gte__lte=date(1999, 12, 31),
            )



