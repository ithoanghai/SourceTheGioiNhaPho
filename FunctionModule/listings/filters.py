
from django_filters import FilterSet, CharFilter, BaseInFilter

from FunctionModule.listings.models import Listing

class MultipleCharFilter(BaseInFilter, CharFilter):
    pass


class ListingFilter(FilterSet):
    realtor = CharFilter(field_name='realtor', lookup_expr='iexact')
    transaction_type = MultipleCharFilter(field_name='transaction_type')

    class Meta:
        model = Listing
        fields = ['realtor', 'transaction_type', 'registration_type']
