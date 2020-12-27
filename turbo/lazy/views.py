import base64
import importlib
import json

from django.http import HttpResponse
from django.shortcuts import render


def lazy(request):
    token = decode(request.GET['token'])

    context = json.loads(token)

    print(f"Context: {context}")

    id = context.get('id')
    view = context.get('view')
    args = context.get('args')
    kwargs = context.get('kwargs')

    view_parts = view.split(".")
    module_name = '.'.join(view_parts[:-1])
    function = view_parts[-1]

    module = importlib.import_module(module_name)
    method_to_call = getattr(module, function)
    if id is None:
        return method_to_call(request, *args, **kwargs)
    else:
        response = method_to_call(request, *args, **kwargs)
        return render(request, 'lazy/turbo_frame.html', {"id": id, "content": response.content.decode('utf-8')})


def decode(base_string) -> str:
    return base64.b64decode(bytes(base_string, 'utf-8')).decode('utf-8')


def encode(s) -> str:
    return base64.b64encode(bytes(s, 'utf-8')).decode('utf-8')
