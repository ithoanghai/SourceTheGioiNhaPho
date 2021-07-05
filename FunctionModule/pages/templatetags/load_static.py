import functools
import json

from django import template
from django.conf import settings
from django.template.base import TextNode
from django.templatetags.static import StaticNode

register = template.Library()


@functools.cache
def get_manifest(static_type):
    try:
        with open(f'{settings.STATIC_ROOT}/{static_type}/manifest.json') as fp:
            manifest = json.load(fp)
            return manifest
    except (FileNotFoundError, NotADirectoryError):
        return {}
    except Exception as ex:
        print('Error getting manifest: ', type(ex))
        return {}


def get_url(s):
    s = s.strip('"\'')
    url = StaticNode.handle_simple(s)
    return url


@functools.lru_cache()
def get_minified_url(s: str):
    s = s.strip('"\'')
    bits = s.split('/')
    static_type = bits[0]
    name = bits[1]
    manifest = get_manifest(static_type)
    compiled_name = manifest.get(name, name)
    url = StaticNode.handle_simple(f'{static_type}/{compiled_name}')
    return url


class CustomStaticNode(TextNode):

    def render(self, context):
        return get_url(self.s)


if settings.ENVIRONMENT == 'production':
    def p_render(self, context):
        return get_minified_url(self.s)


    CustomStaticNode.render = p_render


@register.tag('load_static')
def tag_load_static(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError(
            "'%s' takes at least one argument (path to file)" % bits[0])
    return CustomStaticNode(bits[1])
