import datetime
from django.contrib.admin import SimpleListFilter, ChoicesFieldListFilter, BooleanFieldListFilter, DateFieldListFilter, \
    FieldListFilter, ListFilter
from django_filters import FilterSet, CharFilter, BaseInFilter, RangeFilter, NumberFilter
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
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


class ChoicesFieldListFilter(ChoicesFieldListFilter):
    template = 'admin/dropdown_filter.html'

    def choices(self, changelist):
        yield {
            'selected': self.lookup_val is None,
            'query_string': changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('Tất cả')
        }
        none_title = ''
        for lookup, title in self.field.flatchoices:
            if lookup is None:
                none_title = title
                continue
            yield {
                'selected': str(lookup) == self.lookup_val,
                'query_string': changelist.get_query_string({self.lookup_kwarg: lookup}, [self.lookup_kwarg_isnull]),
                'display': title,
            }
        if none_title:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': changelist.get_query_string({self.lookup_kwarg_isnull: 'True'}, [self.lookup_kwarg]),
                'display': none_title,
            }


class DateFieldListFilter(FieldListFilter):
    template = 'admin/dropdown_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_generic = '%s__' % field_path
        self.date_params = {k: v for k, v in params.items() if k.startswith(self.field_generic)}

        now = timezone.now()
        # When time zone support is enabled, convert "now" to the user's time
        # zone so Django's definition of "Today" matches what the user expects.
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        if isinstance(field, models.DateTimeField):
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:       # field is a models.DateField
            today = now.date()
        tomorrow = today + datetime.timedelta(days=1)
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
            prev_month = today.replace(month=today.month - 1, day=1)
        elif today.month == 1:
            next_month = today.replace(month=today.month + 1, day=1)
            prev_month = today.replace(year=today.year - 1, month=12, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
            prev_month = today.replace(month=today.month - 1, day=1)
        next_year = today.replace(year=today.year + 1, month=1, day=1)
        prev_year = today.replace(year=today.year - 1, month=1, day=1)

        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_until = '%s__lt' % field_path
        self.links = (
            (_('Ngày bất kỳ'), {}),
            (_('Today'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('7 ngày trước'), {
                self.lookup_kwarg_since: str(today - datetime.timedelta(days=7)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Tháng này'), {
                self.lookup_kwarg_since: str(today.replace(day=1)),
                self.lookup_kwarg_until: str(next_month),
            }),
            (_('Tháng trước'), {
                self.lookup_kwarg_since: str(prev_month),
                self.lookup_kwarg_until: str(today.replace(day=1)),
            }),
            (_('Năm này'), {
                self.lookup_kwarg_since: str(today.replace(month=1, day=1)),
                self.lookup_kwarg_until: str(next_year),
            }),
            (_('Năm trước'), {
                self.lookup_kwarg_since: str(prev_year),
                self.lookup_kwarg_until: str(today.replace(month=1, day=1)),
            }),
        )
        if field.null:
            self.lookup_kwarg_isnull = '%s__isnull' % field_path
            self.links += (
                (_('Không có ngày'), {self.field_generic + 'isnull': 'True'}),
                (_('Có ngày'), {self.field_generic + 'isnull': 'False'}),
            )
        super().__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        params = [self.lookup_kwarg_since, self.lookup_kwarg_until]
        if self.field.null:
            params.append(self.lookup_kwarg_isnull)
        return params

    def choices(self, changelist):
        for title, param_dict in self.links:
            yield {
                'selected': self.date_params == param_dict,
                'query_string': changelist.get_query_string(param_dict, [self.field_generic]),
                'display': title,
            }


FieldListFilter.register(
    lambda f: isinstance(f, models.DateField), DateFieldListFilter)


class BooleanFieldListFilter(BooleanFieldListFilter):
    template = 'admin/dropdown_filter.html'

    def choices(self, changelist):
        for lookup, title in (
                (None, _('Tất cả')),
                ('1', _('Có')),
                ('0', _('Không'))):
            yield {
                'selected': self.lookup_val == lookup and not self.lookup_val2,
                'query_string': changelist.get_query_string({self.lookup_kwarg: lookup}, [self.lookup_kwarg2]),
                'display': title,
            }


