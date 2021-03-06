from django import forms
from django.db.models import fields
from django.contrib.auth import password_validation

#
from . import models

class LoginForm(forms.Form):
    
    """ Login Form """

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "t-w-full t-font-medium t-rounded-sm t-py-5 t-border t-px-[1rem] t-text-lg"
                }))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "t-w-full t-font-medium t-rounded-sm t-py-5 t-border t-px-[1rem] t-text-lg" 
                }))

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password) :
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("패스워드가 틀렸습니다"))

        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("존재하지 않는 유저입니다"))


class SignUpForm(forms.ModelForm):

    """ SignUp Form """

    class Meta:
        model = models.User
        fields = ("first_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "Name",
                "class": "t-w-full t-font-medium t-rounded-sm t-py-5 t-border t-px-[1rem] t-text-lg"
                }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Email",
                "class": "t-w-full t-font-medium t-rounded-sm t-py-5 t-border t-px-[1rem] t-text-lg"
                })
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "class": "t-w-full t-font-medium t-rounded-sm t-py-5 t-border t-px-[1rem] t-text-lg"
            })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm Password",
            "class": "t-w-full t-font-medium t-rounded-sm t-py-5 t-border t-px-[1rem] t-text-lg"
            })
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "이메일이 이미 존재합니다.", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다")
        else:
            return password
    
    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()