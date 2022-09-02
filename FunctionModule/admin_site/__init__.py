from FunctionModule.admin_site.decorators import register
from FunctionModule.admin_site.filters import (
    AllValuesFieldListFilter, BooleanFieldListFilter, ChoicesFieldListFilter,
    DateFieldListFilter, EmptyFieldListFilter, FieldListFilter, ListFilter,
    RelatedFieldListFilter, RelatedOnlyFieldListFilter, SimpleListFilter,
)
from FunctionModule.admin_site.options import (
    HORIZONTAL, VERTICAL, ModelAdmin, StackedInline, TabularInline,
)
from FunctionModule.admin_site.sites import AdminSites, site
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
    autodiscover_modules('FunctionModule', register_to=site)


default_app_config = 'FunctionModule.admin_site.apps.AdminConfig'
