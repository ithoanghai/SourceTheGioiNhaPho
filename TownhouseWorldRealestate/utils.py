import base64
import importlib
import json
import os
import random
from collections import OrderedDict
from urllib.parse import urlsplit

import django
from django.contrib.sites.models import Site
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.core.files.storage import default_storage
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import FileField
from django.db.models.fields import (
    BinaryField,
    DateField,
    DateTimeField,
    EmailField,
    TimeField,
)
from django.utils import dateparse
from django.utils.encoding import force_bytes, force_str


def import_attribute(path):
    assert isinstance(path, str)
    pkg, attr = path.rsplit(".", 1)
    ret = getattr(importlib.import_module(pkg), attr)
    return ret


def import_callable(path_or_callable):
    if not hasattr(path_or_callable, "__call__"):
        ret = import_attribute(path_or_callable)
    else:
        ret = path_or_callable
    return ret


SERIALIZED_DB_FIELD_PREFIX = "_db_"


def serialize_instance(instance):
    """
    Since Django 1.6 items added to the session are no longer pickled,
    but JSON encoded by default. We are storing partially complete models
    in the session (user, account, token, ...). We cannot use standard
    Django serialization, as these are models are not "complete" yet.
    Serialization will start complaining about missing relations et al.
    """
    data = {}
    for k, v in instance.__dict__.items():
        if k.startswith("_") or callable(v):
            continue
        try:
            field = instance._meta.get_field(k)
            if isinstance(field, BinaryField):
                v = force_str(base64.b64encode(v))
            elif isinstance(field, FileField):
                if v and not isinstance(v, str):
                    v = v.name
            # Check if the field is serializable. If not, we'll fall back
            # to serializing the DB values which should cover most use cases.
            try:
                json.dumps(v, cls=DjangoJSONEncoder)
            except TypeError:
                v = field.get_prep_value(v)
                k = SERIALIZED_DB_FIELD_PREFIX + k
        except FieldDoesNotExist:
            pass
        data[k] = v
    return json.loads(json.dumps(data, cls=DjangoJSONEncoder))


def deserialize_instance(model, data):
    ret = model()
    for k, v in data.items():
        is_db_value = False
        if k.startswith(SERIALIZED_DB_FIELD_PREFIX):
            k = k[len(SERIALIZED_DB_FIELD_PREFIX) :]
            is_db_value = True
        if v is not None:
            try:
                f = model._meta.get_field(k)
                if isinstance(f, DateTimeField):
                    v = dateparse.parse_datetime(v)
                elif isinstance(f, TimeField):
                    v = dateparse.parse_time(v)
                elif isinstance(f, DateField):
                    v = dateparse.parse_date(v)
                elif isinstance(f, BinaryField):
                    v = force_bytes(base64.b64decode(force_bytes(v)))
                elif is_db_value:
                    try:
                        # This is quite an ugly hack, but will cover most
                        # use cases...
                        # The signature of `from_db_value` changed in Django 3
                        # https://docs.djangoproject.com/en/3.0/releases/3.0/#features-removed-in-3-0
                        if django.VERSION < (3, 0):
                            v = f.from_db_value(v, None, None, None)
                        else:
                            v = f.from_db_value(v, None, None)
                    except Exception:
                        raise ImproperlyConfigured(
                            "Unable to auto serialize field '{}', custom"
                            " serialization override required".format(k)
                        )
            except FieldDoesNotExist:
                pass
        setattr(ret, k, v)
    return ret


def set_form_field_order(form, field_order):
    """
    This function is a verbatim copy of django.forms.Form.order_fields() to
    support field ordering below Django 1.9.

    field_order is a list of field names specifying the order. Append fields
    not included in the list in the default order for backward compatibility
    with subclasses not overriding field_order. If field_order is None, keep
    all fields in the order defined in the class. Ignore unknown fields in
    field_order to allow disabling fields in form subclasses without
    redefining ordering.
    """
    if field_order is None:
        return
    fields = OrderedDict()
    for key in field_order:
        try:
            fields[key] = form.fields.pop(key)
        except KeyError:  # ignore unknown fields
            pass
    fields.update(form.fields)  # add remaining fields in original order
    form.fields = fields


def build_absolute_uri(request, location, protocol=None):
    """request.build_absolute_uri() helper

    Like request.build_absolute_uri, but gracefully handling
    the case where request is None.
    """
    from FunctionModule.accounts import app_settings as account_settings

    if request is None:
        site = Site.objects.get_current()
        bits = urlsplit(location)
        if not (bits.scheme and bits.netloc):
            uri = "{proto}://{domain}{url}".format(
                proto=account_settings.DEFAULT_HTTP_PROTOCOL,
                domain=site.domain,
                url=location,
            )
        else:
            uri = location
    else:
        uri = request.build_absolute_uri(location)
    # NOTE: We only force a protocol if we are instructed to do so
    # (via the `protocol` parameter, or, if the default is set to
    # HTTPS. The latter keeps compatibility with the debatable use
    # case of running your site under both HTTP and HTTPS, where one
    # would want to make sure HTTPS links end up in password reset
    # mails even while they were initiated on an HTTP password reset
    # form.
    if not protocol and account_settings.DEFAULT_HTTP_PROTOCOL == "https":
        protocol = account_settings.DEFAULT_HTTP_PROTOCOL
    # (end NOTE)
    if protocol:
        uri = protocol + ":" + uri.partition(":")[2]
    return uri


def get_form_class(forms, form_id, default_form):
    form_class = forms.get(form_id, default_form)
    if isinstance(form_class, str):
        form_class = import_attribute(form_class)
    return form_class


def get_request_param(request, param, default=None):
    if request is None:
        return default
    return request.POST.get(param) or request.GET.get(param, default)


def phone_random(length):
    number = '0123456789'
    #alpha = 'abcdefghijklmnopqrstuvwxyz'
    id = '09'
    for i in range(0,length-2):
        id += random.choice(number)
        #id += random.choice(alpha)
    return id


def file_cleanup(sender, **kwargs):
        """
        File cleanup callback used to emulate the old delete
        behavior using signals. Initially django deleted linked
        files when an object containing a File/ImageField was deleted.

        Usage:
        >>> from django.db.models.signals import post_delete
        >>> post_delete.connect(file_cleanup, sender=MyModel, dispatch_uid="mymodel.file_cleanup")
        """
        for fieldname in sender._meta.get_all_field_names():
            try:
                field = sender._meta.get_field(fieldname)
            except:
                field = None

        if field and isinstance(field, FileField):
            inst = kwargs["instance"]
            f = getattr(inst, fieldname)
            m = inst.__class__._default_manager
            if (
                    hasattr(f, "path")
                    and os.path.exists(f.path)
                    and not m.filter(
                **{"%s__exact" % fieldname: getattr(inst, fieldname)}
            ).exclude(pk=inst._get_pk_val())
            ):
                try:
                    default_storage.delete(f.path)
                except:
                    pass