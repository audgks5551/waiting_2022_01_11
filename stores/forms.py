from django import forms
from . import models


class CreateStoreForm(forms.ModelForm):

    class Meta:
        model = models.Store
        fields = (
            "name",
            "address",
            "phone_number",
            "store_type",
            "food_type",
            "menu",
            "themes",
            "tastes",
            "amenities",
            "tags",
        )
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "가게 이름", }),
            "address": forms.TextInput(attrs={"placeholder": "가게 주소", }),
            "store_type": forms.Select(),
            "food_type": forms.Select(),
            "menu": forms.Select(),
            "amenities": forms.CheckboxSelectMultiple(),
            "themes": forms.CheckboxSelectMultiple(),
            "tastes": forms.CheckboxSelectMultiple(),
            "tags": forms.TextInput(attrs={"placeholder": "태그", }),
            "phone_number": forms.TextInput(attrs={"placeholder": "전화번호", }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "가게 이름"
        self.fields["address"].label = "가게 주소"
        self.fields["store_type"].label = "음식 종류"
        self.fields["food_type"].label = "음식 상세 종류"
        self.fields["menu"].label = "대표 음식"
        self.fields["amenities"].label = "편의 시설 (여러 개 선택 가능)"
        self.fields["themes"].label = "테마 (여러 개 선택 가능)"
        self.fields["tastes"].label = "맛 (여러 개 선택 가능)"
        self.fields["tags"].label = "태그 - 많이 쓰실 수록 검색할 때 용이합니다 ('/'를 기준으로)"
        self.fields["phone_number"].label = "전화번호"


class AddPhotoForm(forms.ModelForm):

    class Meta:
        model = models.Image
        fields = (
            "file",
        )
        widgets = {
            "file": forms.ClearableFileInput(attrs={"name": "images", "multiple": True, }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].label = ""


class SearchForm(forms.Form):

    #store_type = forms.ModelMultipleChoiceField(
    #    required=False, queryset=models.StoreType.objects.all(), widget=forms.CheckboxSelectMultiple,
    #)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    themes = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Theme.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    tastes = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Taste.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields["store_type"].label = "음식"
        #self.fields["store_type"].label_suffix = ""
        self.fields["amenities"].label = "서비스"
        self.fields["amenities"].label_suffix = ""
        self.fields["themes"].label = "테마"
        self.fields["themes"].label_suffix = ""
        self.fields["tastes"].label = "맛"
        self.fields["tastes"].label_suffix = ""
