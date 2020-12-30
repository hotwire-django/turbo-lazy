import random
from time import sleep

from django.forms import TextInput
from django.shortcuts import render, redirect

from apps.streams.response import TurboFrameTemplateResponse

from apps.streams.response import TurboStreamTemplateResponse
from django.views.generic import CreateView, UpdateView

from apps.demo.models import Entry

from .forms import EntryForm
from django.views.generic.base import View

from apps.streams.mixins import TurboStreamFormMixin


def index(request):
    form = EntryForm()
    return render(request, 'demo/index.html', {"numbers": [i for i in range(0, 10)], "form": form})


def lazy_loaded(request, number):
    # wait to simulate long request
    wait_seconds = random.randint(1, 5)
    sleep(wait_seconds)
    return render(request, 'demo/_final.html', {"id": number})


def submit(request):
    print(f'Got Submission: {request.POST}')
    print(f'Headers: {request.headers.get("Accept")}')
    if not hasattr(request, "accept_turbo_stream"):
        print("No accept_turbo_stream!")
        return redirect('index')
    print(f'Accepts: {request.accept_turbo_stream}')

    f = EntryForm(request.POST)

    # if request.accept_turbo_stream:
    #     print(f'Returning the Turbo Frame...')
    #     return TurboStreamTemplateResponse(
    #         request,
    #         "demo/replacement.html",
    #         {},
    #         action="update",
    #         target="my_form_content",
    #     )
    # else:
    return redirect('index')


class NewEntryStreams(TurboStreamFormMixin, CreateView):
    model = Entry
    fields = ("name", "email", "job_title", "bio")

    def get_turbo_stream_target(self):
        return "my_form_123"

    def get_turbo_stream_template(self):
        return 'demo/entry_form.html'

    def get_success_url(self):
        return 'index'


class NewEntry(CreateView):
    model = Entry
    fields = ("id", "name", "email", "job_title", "bio")

    def get_success_url(self):
        return '/list'


class UpdateEntry(UpdateView):
    model = Entry
    fields = ("id", "name", "email", "job_title", "bio")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_template_names(self):
        return ('demo/entry_update_form.html',)

    def get_success_url(self):
        return '/list'


def new_entry(request):
    if request.method == "GET":
        return render(request, 'demo/entry_form.html', {"form": EntryForm(initial={})})
    elif request.method == "POST":
        form: EntryForm = EntryForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect('index')
            except Exception as e:
                return render(request, 'demo/entry_form.html', {"form": form, "exception": e})
        else:
            return TurboStreamTemplateResponse(request, 'demo/entry_form.html', {"form": form}, "replace",
                                               "my_form_123")


def list_entries(request):
    return render(request, 'demo/crud.html', {"entities": Entry.objects.all()})
