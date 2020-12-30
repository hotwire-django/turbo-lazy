from django.contrib import admin

# Register your models here.
from apps.demo.models import Entry

admin.site.register(Entry)
