from django.db import models
from django.db.models import Model, Q


class Entry(Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=130, unique=True)
    email = models.EmailField(blank=True)
    job_title = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)

    # def validate_unique(self, exclude=None):
    #     exists = Entry.objects\
    #         .filter(Q(name=self.name))\
    #         .exclude(id=self.id)\
    #         .exists()
    #     # return super().validate_unique("name")
    #     validate_unique = super().validate_unique(exclude)
    #     return validate_unique


