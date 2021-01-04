import importlib
import inspect

from django import template
from django.template.response import TemplateResponse
from django.urls import resolve, Resolver404
from tag_parser.basetags import BaseNode

register = template.Library()


@register.tag("include_view")
class ImportViewNode(BaseNode):
    min_args = 1
    max_args = None
    allowed_kwargs = None

    #
    # def __init__(self, view, all_args):
    #     self.view = view
    #     self.all_args = all_args

    def render_tag(self, context, *tag_args, **tag_kwargs):
        method_call = None
        args = None
        kwargs = None
        if len(tag_args) == 1:
            # Try to resolve
            try:
                resolver_match = resolve(tag_args[0])
                method_call = resolver_match.func
                args = resolver_match.args
                kwargs = resolver_match.kwargs
            except Resolver404:
                pass
        if method_call is None:
            view_name = tag_args[0]

            args = tag_args[1:]
            kwargs = tag_kwargs
            view_parts = view_name.split(".")
            module_name = '.'.join(view_parts[:-1])
            function = view_parts[-1]

            module = importlib.import_module(module_name)
            view_object = getattr(module, function)

            if inspect.isclass(view_object):
                method_call = view_object.as_view()
            elif callable(view_object):
                method_call = view_object
            else:
                raise Exception("WHat should this be??")
        request = context.request
        response = method_call(request, *args, **kwargs)
        if isinstance(response, TemplateResponse):
            response.render()
        content = response.content.decode("utf-8")
        return content
