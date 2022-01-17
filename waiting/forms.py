from django import forms
from . import models


class StartWaitingForm(forms.ModelForm):

    class Meta:
        model = models.StartWaiting
        fields = (
            "wait_time",
            "table_number",
            "phone_number",
        )
        widgets = {
            "wait_time": forms.TextInput(attrs={"placeholder": "한 테이블 당 식사시간", }),
            "table_number": forms.TextInput(attrs={"placeholder": "테이블 수", }),
            "phone_number": forms.TextInput(attrs={"placeholder": "전화번호", }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["wait_time"].label = "한 테이블 당 식사시간"
        self.fields["table_number"].label = "테이블 수"
        self.fields["phone_number"].label = "전화번호"


class WaitingForm(forms.ModelForm):

    class Meta:
        model = models.Waiting
        fields = ("people_number", )
        widgets = {
            "people_number": forms.NumberInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["people_number"].label = "인원 수"
