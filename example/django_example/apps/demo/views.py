import random
from time import sleep

from django.shortcuts import render


def index(request):
    return render(request, 'demo/index.html', { "numbers": [i for i in range(0, 10)]})


def lazy_loaded(request, number):
    # wait to simulate long request
    wait_seconds = random.randint(1,5)
    sleep(wait_seconds)
    return render(request, 'demo/_final.html', {"id": number})