from django import forms

from .models import Entry

class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ['name', 'email', 'job_title', 'bio']
#
#
# class EntryUpdateForm(forms.ModelForm):
#
#     class Meta:
#         model = Entry
#         fields = ['id', 'name', 'email', 'job_title', 'bio']



















