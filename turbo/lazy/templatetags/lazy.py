import importlib
import json
import uuid

from django import template
from django.template.base import Token
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe

import turbo
from turbo.lazy.views import encode

register = template.Library()


@register.simple_tag
def lazy_import():
    """
    Automatically adds the script tag with the CDN link for the Import section (should be in the header)
    """
    return render_to_string('lazy/lazy_import.html')


def get_view_path():
    try:
        return reverse(turbo.lazy.views.lazy)
    except Exception:
        raise Exception("Do you have the view function 'turbo.lazy.views.lazy' wired up in your URL configuration?")


@register.simple_tag
def lazy_link(view_name, *args, **kwargs):
    base_string = json.dumps({"view": view_name, "args": args, "kwargs": kwargs})
    return f'{get_view_path()}?token={encode(base_string)}'


@register.simple_tag
def turbo_frame_link(id, view_name, *args, **kwargs):
    base_string = json.dumps({"id": id, "view": view_name, "args": args, "kwargs": kwargs})
    return f'{get_view_path()}?token={encode(base_string)}'


@register.tag("lazy")
def lazy(parser, token: Token):
    """
    The syntax is as follows:
    `{% lazy '<full path to a view function>' arg1=... ... argN=... key1=... ... keyN=... %}`
    for example:
    `{% lazy 'apps.core.partial_views._machine_card' poll_status.machine_id %}`
    This would lazy load the view function `apps.core.partial_views._machine_card` with the arguments `request`
    and positional argument loaded from `poll_status.machine_id`.
    :param parser:
    :param token:
    :return:
    """
    nodelist = parser.parse(('endlazy',))
    parser.delete_first_token()
    return LazyNode(token.split_contents()[1:], nodelist)


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def resolve_from_context(context, arg):
    if arg.__contains__('.'):
        key = arg.split('.')[0]
        tail = '.'.join(arg.split('.')[1:])
        return resolve_from_context(context.get(key), tail)
    else:
        return context.get(arg)


def resolve_single_arg(context, arg: str):
    if not arg.startswith("'") and not arg.startswith('"') and not is_int(arg):
        return resolve_from_context(context, arg)
    else:
        return arg.strip("'").strip('"')


def resolve_args(context, args):
    return [resolve_single_arg(context, arg) for arg in args]


class LazyNode(template.Node):

    def __init__(self, token, nodelist):
        self.nodelist = nodelist
        self.view = token[0].strip("'").strip('"')
        self.args = token[1:]

    def render(self, context):
        uid = str(uuid.uuid4())
        resolved_args = resolve_args(context, self.args)
        template_context = {"id": uid,
                            "src": turbo_frame_link(uid, self.view, *resolved_args),
                            "content": self.nodelist.render(context)}
        return render_to_string('lazy/turbo_frame.html', template_context)


@register.tag("include_view")
def include_view(parser, token: Token):
    splitted = token.split_contents()[1:]
    assert len(splitted) >= 1
    view = splitted[0].strip("'").strip('"')
    args = splitted[1:]
    return ImportViewNode(view, args)


class ImportViewNode(template.Node):

    def __init__(self, view, all_args):
        self.view = view
        self.all_args = all_args

    def render(self, context):
        view_parts = self.view.split(".")
        module_name = '.'.join(view_parts[:-1])
        function = view_parts[-1]

        module = importlib.import_module(module_name)
        method_to_call = getattr(module, function)
        request = context['request']
        base_string = json.dumps({"view": self.view, "args": self.all_args})
        return f'<a href="{get_view_path()}?token={encode(base_string)}">link</a><br>{method_to_call(request, 1).content.decode("utf-8")}'
