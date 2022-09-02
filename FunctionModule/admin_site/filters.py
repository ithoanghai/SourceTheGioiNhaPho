"""
This encapsulates the logic for displaying filters in the Django admin.
Filters are specified in models with the "list_filter" option.

Each filter subclass knows how to display a filter for a field that passes a
certain test -- e.g. being a DateField or ForeignKey.
"""
import datetime
import django
import pytz
from collections import OrderedDict

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import models
from django.db.models import Max, Min
from django.db.models.fields import DecimalField, FloatField, IntegerField, AutoField
from django.conf import settings
from django.forms import SplitDateTimeField, DateField
from django.forms.forms import BaseForm
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from django.utils.text import slugify

from FunctionModule.admin_site.forms import RangeNumericForm, SliderNumericForm
from .options import IncorrectLookupParameters
from .utils import (get_model_from_relation, prepare_lookup_value, reverse_field_path,)
from .widgets import AdminDateWidget, AdminSplitDateTime


class ListFilter:
    title = None  # Human-readable title to appear in the right sidebar.
    template = 'admin/filter.html'

    def __init__(self, request, params, model, model_admin):
        # This dictionary will eventually contain the request's query string
        # parameters actually used by this filter.
        self.used_parameters = {}
        if self.title is None:
            raise ImproperlyConfigured(
                "The list filter '%s' does not specify a 'title'."
                % self.__class__.__name__
            )

    def has_output(self):
        """
        Return True if some choices would be output for this filter.
        """
        raise NotImplementedError('subclasses of ListFilter must provide a has_output() method')

    def choices(self, changelist):
        """
        Return choices ready to be output in the template.

        `changelist` is the ChangeList to be displayed.
        """
        raise NotImplementedError('subclasses of ListFilter must provide a choices() method')

    def queryset(self, request, queryset):
        """
        Return the filtered queryset.
        """
        raise NotImplementedError('subclasses of ListFilter must provide a queryset() method')

    def expected_parameters(self):
        """
        Return the list of parameter names that are expected from the
        request's query string and that will be used by this filter.
        """
        raise NotImplementedError('subclasses of ListFilter must provide an expected_parameters() method')


class SimpleListFilter(ListFilter):
    # The parameter that should be used in the query string for that filter.
    parameter_name = None

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        if self.parameter_name is None:
            raise ImproperlyConfigured(
                "The list filter '%s' does not specify a 'parameter_name'."
                % self.__class__.__name__
            )
        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value
        lookup_choices = self.lookups(request, model_admin)
        if lookup_choices is None:
            lookup_choices = ()
        self.lookup_choices = list(lookup_choices)

    def has_output(self):
        return len(self.lookup_choices) > 0

    def value(self):
        """
        Return the value (in string format) provided in the request's
        query string for this filter, if any, or None if the value wasn't
        provided.
        """
        return self.used_parameters.get(self.parameter_name)

    def lookups(self, request, model_admin):
        """
        Must be overridden to return a list of tuples (value, verbose value)
        """
        raise NotImplementedError(
            'The SimpleListFilter.lookups() method must be overridden to '
            'return a list of tuples (value, verbose value).'
        )

    def expected_parameters(self):
        return [self.parameter_name]

    def choices(self, changelist):
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string(remove=[self.parameter_name]),
            'display': _('All'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == str(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }


class FieldListFilter(ListFilter):
    _field_list_filters = []
    _take_priority_index = 0

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field = field
        self.field_path = field_path
        self.title = getattr(field, 'verbose_name', field_path)
        super().__init__(request, params, model, model_admin)
        for p in self.expected_parameters():
            if p in params:
                value = params.pop(p)
                self.used_parameters[p] = prepare_lookup_value(p, value)

    def has_output(self):
        return True

    def queryset(self, request, queryset):
        try:
            return queryset.filter(**self.used_parameters)
        except (ValueError, ValidationError) as e:
            # Fields may raise a ValueError or ValidationError when converting
            # the parameters to the correct type.
            raise IncorrectLookupParameters(e)

    @classmethod
    def register(cls, test, list_filter_class, take_priority=False):
        if take_priority:
            # This is to allow overriding the default filters for certain types
            # of fields with some custom filters. The first found in the list
            # is used in priority.
            cls._field_list_filters.insert(
                cls._take_priority_index, (test, list_filter_class))
            cls._take_priority_index += 1
        else:
            cls._field_list_filters.append((test, list_filter_class))

    @classmethod
    def create(cls, field, request, params, model, model_admin, field_path):
        for test, list_filter_class in cls._field_list_filters:
            if test(field):
                return list_filter_class(field, request, params, model, model_admin, field_path=field_path)


class RelatedFieldListFilter(FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        other_model = get_model_from_relation(field)
        self.lookup_kwarg = '%s__%s__exact' % (field_path, field.target_field.name)
        self.lookup_kwarg_isnull = '%s__isnull' % field_path
        self.lookup_val = params.get(self.lookup_kwarg)
        self.lookup_val_isnull = params.get(self.lookup_kwarg_isnull)
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_choices = self.field_choices(field, request, model_admin)
        if hasattr(field, 'verbose_name'):
            self.lookup_title = field.verbose_name
        else:
            self.lookup_title = other_model._meta.verbose_name
        self.title = self.lookup_title
        self.empty_value_display = model_admin.get_empty_value_display()

    @property
    def include_empty_choice(self):
        """
        Return True if a "(None)" choice should be included, which filters
        out everything except empty relationships.
        """
        return self.field.null or (self.field.is_relation and self.field.many_to_many)

    def has_output(self):
        if self.include_empty_choice:
            extra = 1
        else:
            extra = 0
        return len(self.lookup_choices) + extra > 1

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_isnull]

    def field_admin_ordering(self, field, request, model_admin):
        """
        Return the model admin's ordering for related field, if provided.
        """
        related_admin = model_admin.admin_site._registry.get(field.remote_field.model)
        if related_admin is not None:
            return related_admin.get_ordering(request)
        return ()

    def field_choices(self, field, request, model_admin):
        ordering = self.field_admin_ordering(field, request, model_admin)
        return field.get_choices(include_blank=False, ordering=ordering)

    def choices(self, changelist):
        yield {
            'selected': self.lookup_val is None and not self.lookup_val_isnull,
            'query_string': changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All'),
        }
        for pk_val, val in self.lookup_choices:
            yield {
                'selected': self.lookup_val == str(pk_val),
                'query_string': changelist.get_query_string({self.lookup_kwarg: pk_val}, [self.lookup_kwarg_isnull]),
                'display': val,
            }
        if self.include_empty_choice:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': changelist.get_query_string({self.lookup_kwarg_isnull: 'True'}, [self.lookup_kwarg]),
                'display': self.empty_value_display,
            }


FieldListFilter.register(lambda f: f.remote_field, RelatedFieldListFilter)


class BooleanFieldListFilter(FieldListFilter):
    template = 'admin/dropdown_filter.html'
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = '%s__exact' % field_path
        self.lookup_kwarg2 = '%s__isnull' % field_path
        self.lookup_val = params.get(self.lookup_kwarg)
        self.lookup_val2 = params.get(self.lookup_kwarg2)
        super().__init__(field, request, params, model, model_admin, field_path)
        if (self.used_parameters and self.lookup_kwarg in self.used_parameters and
                self.used_parameters[self.lookup_kwarg] in ('1', '0')):
            self.used_parameters[self.lookup_kwarg] = bool(int(self.used_parameters[self.lookup_kwarg]))

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg2]

    def choices(self, changelist):
        for lookup, title in (
                (None, _('All')),
                ('1', _('Yes')),
                ('0', _('No'))):
            yield {
                'selected': self.lookup_val == lookup and not self.lookup_val2,
                'query_string': changelist.get_query_string({self.lookup_kwarg: lookup}, [self.lookup_kwarg2]),
                'display': title,
            }
        if self.field.null:
            yield {
                'selected': self.lookup_val2 == 'True',
                'query_string': changelist.get_query_string({self.lookup_kwarg2: 'True'}, [self.lookup_kwarg]),
                'display': _('Unknown'),
            }


FieldListFilter.register(lambda f: isinstance(f, models.BooleanField), BooleanFieldListFilter)


class ChoicesFieldListFilter(FieldListFilter):
    template = 'admin/dropdown_filter.html'
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = '%s__exact' % field_path
        self.lookup_kwarg_isnull = '%s__isnull' % field_path
        self.lookup_val = params.get(self.lookup_kwarg)
        self.lookup_val_isnull = params.get(self.lookup_kwarg_isnull)
        super().__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_isnull]

    def choices(self, changelist):
        yield {
            'selected': self.lookup_val is None,
            'query_string': changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All')
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


FieldListFilter.register(lambda f: bool(f.choices), ChoicesFieldListFilter)


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
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        next_year = today.replace(year=today.year + 1, month=1, day=1)

        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_until = '%s__lt' % field_path
        self.links = (
            (_('Ngày bất kỳ'), {}),
            (_('Today'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Past 7 days'), {
                self.lookup_kwarg_since: str(today - datetime.timedelta(days=7)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('This month'), {
                self.lookup_kwarg_since: str(today.replace(day=1)),
                self.lookup_kwarg_until: str(next_month),
            }),
            (_('This year'), {
                self.lookup_kwarg_since: str(today.replace(month=1, day=1)),
                self.lookup_kwarg_until: str(next_year),
            }),
        )
        if field.null:
            self.lookup_kwarg_isnull = '%s__isnull' % field_path
            self.links += (
                (_('No date'), {self.field_generic + 'isnull': 'True'}),
                (_('Has date'), {self.field_generic + 'isnull': 'False'}),
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


# This should be registered last, because it's a last resort. For example,
# if a field is eligible to use the BooleanFieldListFilter, that'd be much
# more appropriate, and the AllValuesFieldListFilter won't get used for it.
class AllValuesFieldListFilter(FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = field_path
        self.lookup_kwarg_isnull = '%s__isnull' % field_path
        self.lookup_val = params.get(self.lookup_kwarg)
        self.lookup_val_isnull = params.get(self.lookup_kwarg_isnull)
        self.empty_value_display = model_admin.get_empty_value_display()
        parent_model, reverse_path = reverse_field_path(model, field_path)
        # Obey parent ModelAdmin queryset when deciding which options to show
        if model == parent_model:
            queryset = model_admin.get_queryset(request)
        else:
            queryset = parent_model._default_manager.all()
        self.lookup_choices = queryset.distinct().order_by(field.name).values_list(field.name, flat=True)
        super().__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_isnull]

    def choices(self, changelist):
        yield {
            'selected': self.lookup_val is None and self.lookup_val_isnull is None,
            'query_string': changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All'),
        }
        include_none = False
        for val in self.lookup_choices:
            if val is None:
                include_none = True
                continue
            val = str(val)
            yield {
                'selected': self.lookup_val == val,
                'query_string': changelist.get_query_string({self.lookup_kwarg: val}, [self.lookup_kwarg_isnull]),
                'display': val,
            }
        if include_none:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': changelist.get_query_string({self.lookup_kwarg_isnull: 'True'}, [self.lookup_kwarg]),
                'display': self.empty_value_display,
            }


FieldListFilter.register(lambda f: True, AllValuesFieldListFilter)


class RelatedOnlyFieldListFilter(RelatedFieldListFilter):
    def field_choices(self, field, request, model_admin):
        pk_qs = model_admin.get_queryset(request).distinct().values_list('%s__pk' % self.field_path, flat=True)
        ordering = self.field_admin_ordering(field, request, model_admin)
        return field.get_choices(include_blank=False, limit_choices_to={'pk__in': pk_qs}, ordering=ordering)


class EmptyFieldListFilter(FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        if not field.empty_strings_allowed and not field.null:
            raise ImproperlyConfigured(
                "The list filter '%s' cannot be used with field '%s' which "
                "doesn't allow empty strings and nulls." % (
                    self.__class__.__name__,
                    field.name,
                )
            )
        self.lookup_kwarg = '%s__isempty' % field_path
        self.lookup_val = params.get(self.lookup_kwarg)
        super().__init__(field, request, params, model, model_admin, field_path)

    def queryset(self, request, queryset):
        if self.lookup_kwarg not in self.used_parameters:
            return queryset
        if self.lookup_val not in ('0', '1'):
            raise IncorrectLookupParameters

        lookup_condition = models.Q()
        if self.field.empty_strings_allowed:
            lookup_condition |= models.Q(**{self.field_path: ''})
        if self.field.null:
            lookup_condition |= models.Q(**{'%s__isnull' % self.field_path: True})
        if self.lookup_val == '1':
            return queryset.filter(lookup_condition)
        return queryset.exclude(lookup_condition)

    def expected_parameters(self):
        return [self.lookup_kwarg]

    def choices(self, changelist):
        for lookup, title in (
            (None, _('All')),
            ('1', _('Empty')),
            ('0', _('Not empty')),
        ):
            yield {
                'selected': self.lookup_val == lookup,
                'query_string': changelist.get_query_string({self.lookup_kwarg: lookup}),
                'display': title,
            }


class DateRangeFilter(FieldListFilter):
    _request_key = "DJANGO_RANGEFILTER_ADMIN_JS_LIST"

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_gte = "{0}__range__gte".format(field_path)
        self.lookup_kwarg_lte = "{0}__range__lte".format(field_path)

        self.default_gte, self.default_lte = self._get_default_values(
            request, model_admin, field_path
        )

        super(DateRangeFilter, self).__init__(
            field, request, params, model, model_admin, field_path
        )
        self.request = request
        self.model_admin = model_admin
        self.form = self.get_form(request)

        custom_title = self._get_custom_title(request, model_admin, field_path)
        if custom_title:
            self.title = custom_title

    def get_timezone(self, _request):
        return timezone.get_default_timezone()

    @staticmethod
    def _get_custom_title(request, model_admin, field_path):
        title_method_name = "get_rangefilter_{0}_title".format(field_path)
        title_method = getattr(model_admin, title_method_name, None)

        if not callable(title_method):
            return None

        return title_method(request, field_path)

    @staticmethod
    def _get_default_values(request, model_admin, field_path):
        default_method_name = "get_rangefilter_{0}_default".format(field_path)
        default_method = getattr(model_admin, default_method_name, None)

        if not callable(default_method):
            return None, None

        return default_method(request)

    @staticmethod
    def make_dt_aware(value, tzname):
        if django.VERSION <= (4, 0, 0):
            if settings.USE_TZ and pytz is not None:
                default_tz = tzname
                if value.tzinfo is not None:
                    value = default_tz.normalize(value)
                else:
                    value = default_tz.localize(value)
        else:
            value = value.replace(tzinfo=tzname)
        return value

    def choices(self, changelist):
        yield {
            # slugify converts any non-unicode characters to empty characters
            # but system_name is required, if title converts to empty string use id
            # https://github.com/silentsokolov/django-admin-rangefilter/issues/18
            "system_name": force_str(
                slugify(self.title) if slugify(self.title) else id(self.title)
            ),
            "query_string": changelist.get_query_string({}, remove=self._get_expected_fields()),
        }

    def expected_parameters(self):
        return self._get_expected_fields()

    def queryset(self, request, queryset):
        if self.form.is_valid():
            validated_data = dict(self.form.cleaned_data.items())
            if validated_data:
                return queryset.filter(**self._make_query_filter(request, validated_data))
        return queryset

    def _get_expected_fields(self):
        return [self.lookup_kwarg_gte, self.lookup_kwarg_lte]

    def _make_query_filter(self, request, validated_data):
        query_params = {}
        date_value_gte = validated_data.get(self.lookup_kwarg_gte, None)
        date_value_lte = validated_data.get(self.lookup_kwarg_lte, None)

        if date_value_gte:
            query_params["{0}__gte".format(self.field_path)] = self.make_dt_aware(
                datetime.datetime.combine(date_value_gte, datetime.time.min),
                self.get_timezone(request),
            )
        if date_value_lte:
            query_params["{0}__lte".format(self.field_path)] = self.make_dt_aware(
                datetime.datetime.combine(date_value_lte, datetime.time.max),
                self.get_timezone(request),
            )

        return query_params

    def get_template(self):
        if django.VERSION[:2] <= (1, 8):
            return "admin/date_filter_1_8.html"

        return "admin/date_filter.html"

    template = property(get_template)

    def get_form(self, _request):
        form_class = self._get_form_class()
        return form_class(self.used_parameters or None)

    def _get_form_class(self):
        fields = self._get_form_fields()

        form_class = type(str("DateRangeForm"), (BaseForm,), {"base_fields": fields})

        # lines below ensure that the js static files are loaded just once
        # even if there is more than one DateRangeFilter in use
        js_list = getattr(self.request, self._request_key, None)

        form_class.js = js_list

        return form_class

    def _get_form_fields(self):
        return OrderedDict(
            (
                (
                    self.lookup_kwarg_gte,
                    DateField(
                        label="",
                        widget=AdminDateWidget(attrs={"placeholder": _("Từ ngày")}),
                        localize=True,
                        required=False,
                        initial=self.default_gte,
                    ),
                ),
                (
                    self.lookup_kwarg_lte,
                    DateField(
                        label="",
                        widget=AdminDateWidget(attrs={"placeholder": _("Đến ngày")}),
                        localize=True,
                        required=False,
                        initial=self.default_lte,
                    ),
                ),
            )
        )


class DateTimeRangeFilter(DateRangeFilter):
    def _get_expected_fields(self):
        expected_fields = []
        for field in [self.lookup_kwarg_gte, self.lookup_kwarg_lte]:
            for i in range(2):
                expected_fields.append("{}_{}".format(field, i))

        return expected_fields

    def _get_form_fields(self):
        return OrderedDict(
            (
                (
                    self.lookup_kwarg_gte,
                    SplitDateTimeField(
                        label="",
                        widget=AdminSplitDateTime(attrs={"placeholder": _("Từ ngày")}),
                        localize=True,
                        required=False,
                        initial=self.default_gte,
                    ),
                ),
                (
                    self.lookup_kwarg_lte,
                    SplitDateTimeField(
                        label="",
                        widget=AdminSplitDateTime(attrs={"placeholder": _("Đến ngày")}),
                        localize=True,
                        required=False,
                        initial=self.default_lte,
                    ),
                ),
            )
        )

    def _make_query_filter(self, request, validated_data):
        query_params = {}
        date_value_gte = validated_data.get(self.lookup_kwarg_gte, None)
        date_value_lte = validated_data.get(self.lookup_kwarg_lte, None)

        if date_value_gte:
            query_params["{0}__gte".format(self.field_path)] = self.make_dt_aware(
                date_value_gte, self.get_timezone(request)
            )
        if date_value_lte:
            query_params["{0}__lte".format(self.field_path)] = self.make_dt_aware(
                date_value_lte, self.get_timezone(request)
            )

        return query_params


class RangeNumericFilter(FieldListFilter):
    request = None
    parameter_name = None
    template = 'admin/filter_numeric_range.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        if not isinstance(field, (DecimalField, IntegerField, FloatField, AutoField)):
            raise TypeError('Class {} is not supported for {}.'.format(type(self.field), self.__class__.__name__))
        self.request = request
        if self.parameter_name is None:
            self.parameter_name = self.field_path

        if self.parameter_name + '_from' in params:
            value = params.pop(self.field_path + '_from')
            self.used_parameters[self.field_path + '_from'] = value

        if self.parameter_name + '_to' in params:
            value = params.pop(self.field_path + '_to')
            self.used_parameters[self.field_path + '_to'] = value

    def queryset(self, request, queryset):
        filters = {}

        value_from = self.used_parameters.get(self.parameter_name + '_from', None)
        if value_from is not None and value_from != '':
            filters.update({
                self.parameter_name + '__gte': self.used_parameters.get(self.parameter_name + '_from', None),
            })

        value_to = self.used_parameters.get(self.parameter_name + '_to', None)
        if value_to is not None and value_to != '':
            filters.update({
                self.parameter_name + '__lte': self.used_parameters.get(self.parameter_name + '_to', None),
            })

        return queryset.filter(**filters)

    def expected_parameters(self):
        return [
            '{}_from'.format(self.parameter_name),
            '{}_to'.format(self.parameter_name),
        ]

    def choices(self, changelist):
        return ({
            'request': self.request,
            'parameter_name': self.parameter_name,
            'form': RangeNumericForm(name=self.parameter_name, data={
                self.parameter_name + '_from': self.used_parameters.get(self.parameter_name + '_from', None),
                self.parameter_name + '_to': self.used_parameters.get(self.parameter_name + '_to', None),
            }),
        }, )


FieldListFilter.register(lambda f: isinstance(f, models.DecimalField), RangeNumericFilter)


class SliderNumericFilter(RangeNumericFilter):
    MAX_DECIMALS = 7
    STEP = None

    template = 'admin/filter_numeric_slider.html'
    field = None

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)

        self.field = field
        self.q = model_admin.get_queryset(request)

    def choices(self, changelist):
        total = self.q.all().count()
        min_value = self.q.all().aggregate(
            min=Min(self.parameter_name)
        ).get('min', 0)

        if total > 1:
            max_value = self.q.all().aggregate(
                max=Max(self.parameter_name)
            ).get('max', 0)
        else:
            max_value = None

        if isinstance(self.field, (FloatField, DecimalField)):
            decimals = self.MAX_DECIMALS
            step = self.STEP if self.STEP else self._get_min_step(self.MAX_DECIMALS)
        else:
            decimals = 0
            step = self.STEP if self.STEP else 1

        return ({
            'decimals': decimals,
            'step': step,
            'parameter_name': self.parameter_name,
            'request': self.request,
            'min': min_value,
            'max': max_value,
            'value_from': self.used_parameters.get(self.parameter_name + '_from', min_value),
            'value_to': self.used_parameters.get(self.parameter_name + '_to', max_value),
            'form': SliderNumericForm(name=self.parameter_name, data={
                self.parameter_name + '_from': self.used_parameters.get(self.parameter_name + '_from', min_value),
                self.parameter_name + '_to': self.used_parameters.get(self.parameter_name + '_to', max_value),
            })
        }, )

    def _get_min_step(self, precision):
        result_format = '{{:.{}f}}'.format(precision - 1)
        return float(result_format.format(0) + '1')