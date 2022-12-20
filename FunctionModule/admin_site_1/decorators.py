def register(*models, site=None):
    """
    Register the given model(s) classes and wrapped ModelAdmin class with
    admin site:

    @register(Author)
    class AuthorAdmin(admin.ModelAdmin):
        pass

    The `site` kwarg is an admin site to use instead of the default admin site.
    """
    from django.contrib.admin import ModelAdmin
    from FunctionModule.admin_site_1.sites import site as default_site, AdminSites

    def _model_admin_wrapper(admin_class):
        if not models:
            raise ValueError('At least one model must be passed to register.')

        admin = site or default_site

        if not isinstance(admin, AdminSites):
            raise ValueError('site must subclass AdminSite')

        if not issubclass(admin_class, ModelAdmin):
            raise ValueError('Wrapped class must subclass ModelAdmin.')

        admin.register(models, admin_class=admin_class)

        return admin_class
    return _model_admin_wrapper