import os
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http.request import HttpRequest
from django.shortcuts import redirect, render, reverse
from django.views.generic import FormView, View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib import messages


#
from . import forms, models, mixins 
from stores import models as stores_models
import requests

class LoginView(mixins.LoggedOutOnlyView, FormView):

    """ Login View"""

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return redirect(self.get_success_url())


def log_out(request: HttpRequest):

    """ Logout View """

    logout(request)
    messages.info(request, "다음에 또 만나요")
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

    """ SignUp View """

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return redirect(self.get_success_url())

def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add succes message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))

# 깃허브
def github_login(request: HttpRequest):

    client_id = os.environ.get("GIT_ID")
    redirect_uri = "http://localhost:8000/users/login/github/callback/"
    scope = "read:user"

    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}")

class GithubException(Exception):
    pass

def github_collback(request: HttpRequest):
    try:
        client_id = os.environ.get("GIT_ID")
        client_secret = os.environ.get("GIT_SECRET")
        code = request.GET.get("code", None)
        redirect_uri = "http://localhost:8000/users/login/github/callback/"
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}&redirect_uri={redirect_uri}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("토큰을 받아올 수 없습니다")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    f"https://api.github.com/user",
                    headers={"Authorization": f"token {access_token}", "Accept": "application/json"}
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name", None)
                    email = profile_json.get("email")
                    if email is None:
                        raise GithubException("이메일 동의를 허락해주세요")
                    bio = profile_json.get("bio", None)
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LoginChoices.GITHUB:
                            raise GithubException("로그인방식이 일치하지 않습니다")
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=email, 
                            email=email, 
                            first_name=name, 
                            bio=bio, 
                            login_method=models.User.LoginChoices.GITHUB,
                            email_verified=True
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"{name}님 환영합니다")
                    return redirect(reverse("core:home"))

                else:
                    raise GithubException("로그인정보를 받아오지 못했습니다")
        else:
            raise GithubException("인가코드를 받아올 수 없습니다")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


# 카카오톡
def kakao_login(request: HttpRequest):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://localhost:8000/users/login/kakao/callback/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )

class KakaoException(Exception):
    pass    

def kakao_collback(request: HttpRequest):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://localhost:8000/users/login/kakao/callback/"
        token_request = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_request = token_request.json()
        error = token_request.get("error", None)
        if error is not None:
            raise KakaoException("토큰을 받아올 수 없습니다")
        access_token = token_request.get("access_token")
        profile_request = requests.get(
            f"https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email")
        if email is None:
            raise KakaoException("이메일 동의를 허락해주세요")
        profile = kakao_account.get("profile")
        print(profile)
        nickname = profile.get("nickname")
        profile_image_url = profile.get("profile_image_url")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LoginChoices.KAKAO:
                raise KakaoException("카카오 로그인 방식이 아닙니다")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                username=email, 
                email=email,
                first_name=nickname,
                login_method=models.User.LoginChoices.KAKAO,
                email_verified=True
            )
            user.set_unusable_password()
            user.save()
            if profile_image_url is not None:
                photo_request = requests.get(profile_image_url)
                user.avatar.save(
                    f"{nickname}-avatar.jpg", ContentFile(photo_request.content)
                )
        login(request, user)
        messages.success(request, f"{nickname}님 환영합니다")
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


@login_required
def showMyPage(request):
    
    """ Show My Page """

    current_user_id = request.user.id
    
    context = {"current_user_id": current_user_id}
    return render(request, "users/users_mypage.html", context)

@login_required
def myStoreList(request):
    
    current_user_id = request.user.id

    myStore_list = stores_models.Store.objects.filter(user_id=current_user_id)

    context = {
        "current_user_id": current_user_id,
        "myStore_list": myStore_list,
    }
    return render(request, "users/users_store_list.html", context)