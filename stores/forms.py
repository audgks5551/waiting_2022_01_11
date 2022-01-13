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
            "name": forms.TextInput(attrs={"placeholder": "가게 이름",}),
            "address": forms.TextInput(attrs={"placeholder": "가게 주소",}),
            "store_type": forms.Select(attrs={"placeholder": "가게 종류",}),
            "food_type": forms.Select(attrs={"placeholder": "음식 종류",}),
            "amenities": forms.CheckboxSelectMultiple(attrs={"placeholder": "편의 시설",}),
            "tags": forms.TextInput(attrs={"placeholder": "태그",}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = ""
        self.fields["address"].label = ""
        self.fields["store_type"].label = "가게 종류"
        self.fields["food_type"].label = "음식 종류"
        self.fields["amenities"].label = "편의 시설 (여러 개 선택 가능)"
        self.fields["tags"].label = "태그 - 많이 쓰실 수록 검색할 때 용이합니다 ('/'를 기준으로)"

class AddPhotoForm(forms.ModelForm):

    class Meta:
        model = models.Image
        fields = (
            "file",
        )
        widgets = {
            "file": forms.ClearableFileInput(attrs={"name": "images", "multiple": True,}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].label = ""  