from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.core.files.base import ContentFile

import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File

#
import qrcode
from . import models
from . import forms
from users import mixins as user_mixins

def listStore(request):

    """ List Store """

    current_user_id = request.user.id

    store_list = models.Store.objects.all()
    
    context = {"store_list": store_list, "current_user_id": current_user_id}
    return render(request, "stores/stores_list.html", context)


def detailStore(request, store_id):

    """ Detail Store """

    current_user_id = request.user.id

    store = models.Store.objects.get(id=store_id)
    
    context = {"store": store, "current_user_id": current_user_id}
    return render(request, "stores/stores_detail.html", context)
    


class createStore(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateStoreForm
    template_name = "stores/stores_create.html"

    def form_valid(self, form):
        store = form.save(commit=False)
        store.user = self.request.user

        store.save()

        url = f"http://127.0.0.1:8000/stores/{store.id}"
        qrcode_img=qrcode.make(url)
        canvas=Image.new("RGB", (500,500),"white")
        draw=ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        buffer=BytesIO()
        canvas.save(buffer,"PNG")
        store.qrcode.save(f'{store.name}-{store.id}.png',File(buffer))
        canvas.close()

        messages.success(self.request, "가게가 생성되었습니다")
        return redirect(reverse("stores:detail", kwargs={"store_id": store.id}))
    
    def get_context_data(self, **kwargs):    
        context = super().get_context_data(**kwargs)                
        context['current_user_id'] = self.request.user.id
        return context