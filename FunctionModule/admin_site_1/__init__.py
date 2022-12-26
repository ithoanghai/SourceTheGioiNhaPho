from django.contrib.admin.decorators import register
from django.contrib.admin.filters import (
    AllValuesFieldListFilter, BooleanFieldListFilter, ChoicesFieldListFilter,
    DateFieldListFilter, EmptyFieldListFilter, FieldListFilter, ListFilter,
    RelatedFieldListFilter, RelatedOnlyFieldListFilter, SimpleListFilter,
)
from django.contrib.admin.options import (
    HORIZONTAL, VERTICAL, ModelAdmin, StackedInline, TabularInline,
)
from FunctionModule.admin_site_1.sites import AdminSites, site
from django.utils.module_loading import autodiscover_modules

__all__ = [
    "register", "ModelAdmin", "HORIZONTAL", "VERTICAL", "StackedInline",
    "TabularInline", "AdminSites", "site", "ListFilter", "SimpleListFilter",
    "FieldListFilter", "BooleanFieldListFilter", "RelatedFieldListFilter",
    "ChoicesFieldListFilter", "DateFieldListFilter",
    "AllValuesFieldListFilter", "EmptyFieldListFilter",
    "RelatedOnlyFieldListFilter", "autodiscover",
]


def autodiscover():
    autodiscover_modules('admin', register_to=site)


default_app_config = 'django.contrib.admin.apps.AdminConfig'
