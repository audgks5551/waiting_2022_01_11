from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse

# qrcode
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File

#
from . import models
from . import forms

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
    images = models.Image.objects.filter(store=store)
    try:
        first_image = images[0]
        images = images[1:]
    except:
        first_image = None
        images = None
        
    context = {
        "store": store, 
        "current_user_id": current_user_id,
        "first_image": first_image,
        "images": images
    }
    
    return render(request, "stores/stores_detail.html", context)
    
def createQRcode(store):
    url = f"http://127.0.0.1:8000/stores/{store.id}"
    qrcode_img=qrcode.make(url)
    canvas=Image.new("RGB", (500,500),"white")
    draw=ImageDraw.Draw(canvas)
    canvas.paste(qrcode_img)
    buffer=BytesIO()
    canvas.save(buffer,"PNG")
    store.qrcode.save(f'{store.name}-{store.id}.png',File(buffer))
    canvas.close()

@login_required
def createStore(request):

    current_user_id = request.user.id

    if request.method == 'POST':
        store_form = forms.CreateStoreForm(request.POST)

        if store_form.is_valid():

            store = store_form.save(commit=False)
            store.user = request.user

            store.save()

            createQRcode(store)

            images = request.FILES.getlist('images')
            if images:
                for image in images:
                    models.Image.objects.create(file=image, store=store)

            messages.success(request, "가게가 생성되었습니다")
            return redirect(reverse("stores:detail", kwargs={"store_id": store.id}))
    else:
        store_form = forms.CreateStoreForm()
        add_photo_form = forms.AddPhotoForm()
    
    context = {
        "store_form": store_form,
        "current_user_id": current_user_id,
        "add_photo_form": add_photo_form
    }   
    return render(request, "stores/stores_create.html", context)