from django import forms
from . import models

class CreateStoreForm(forms.ModelForm):

    class Meta:
        model = models.Store
        fields = ("name",)