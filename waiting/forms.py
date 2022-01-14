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
            "wait_time": forms.TextInput(attrs={"placeholder": "한 테이블 당 식사시간",}),
            "table_number": forms.TextInput(attrs={"placeholder": "테이블 수",}),
            "phone_number": forms.TextInput(attrs={"placeholder": "전화번호",}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["wait_time"].label = ""
        self.fields["table_number"].label = ""
        self.fields["phone_number"].label = ""
