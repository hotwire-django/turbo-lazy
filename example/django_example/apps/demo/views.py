import random
from time import sleep

from apps.streams.response import TurboStreamTemplateResponse
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'demo/index.html', {"numbers": [i for i in range(0, 10)]})


def lazy_loaded(request, number):
    # wait to simulate long request
    wait_seconds = random.randint(1, 5)
    sleep(wait_seconds)
    return render(request, 'demo/_final.html', {"id": number})


def submit(request):
    if not hasattr(request, "accept_turbo_stream"):
        return redirect('index')

    if request.accept_turbo_stream:
        return TurboStreamTemplateResponse(
            request,
            "demo/replacement.html",
            {},
            action="update",
            target="my_form_content",
        )
    else:
        return redirect('index')
