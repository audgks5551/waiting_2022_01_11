from django import forms
from . import models

class CreateStoreForm(forms.ModelForm):

    class Meta:
        model = models.Store
        fields = (
            "name",
            "address",
            "store_type",
            "food_type",
            "amenities",
            "tags"
        )
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "가게 이름",
                "class": "t-w-full t-font-medium t-rounded-sm t-py-5 t-border t-px-[1rem] t-text-lg",
                }),
            "address": forms.TextInput(attrs={
                "placeholder": "가게 주소",
                "class": "t-w-full t-font-medium t-rounded-sm t-py-5 t-border t-px-[1rem] t-text-lg",
                }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = ""
        self.fields["address"].label = ""

class AddPhotoForm(forms.ModelForm):

    class Meta:
        model = models.Image
        fields = (
            "file",
        )
        widgets = {
            "file": forms.ClearableFileInput(attrs={
                "name": "images",
                "multiple": True,
                "class": "t-w-full t-font-medium t-rounded-sm t-py-5 t-border t-px-[1rem] t-text-lg",
                }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].label = ""  