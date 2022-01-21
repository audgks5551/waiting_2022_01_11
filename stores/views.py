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
from waiting import forms as waiting_forms
from waiting import models as waiting_models


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
    waiting_mode = waiting_models.StartWaiting.objects.get(
        store_id=store_id).mode
    context = {
        "store": store,
        "current_user_id": current_user_id,
        "store_id": store_id,
        "waiting_mode": waiting_mode
    }

    return render(request, "stores/stores_detail.html", context)


@login_required
def deleteStore(request, store_id):

    store = models.Store.objects.get(id=store_id)
    store.delete()

    return redirect(reverse("users:my_list"))


@login_required
def modifyStore(request, store_id):

    store = models.Store.objects.get(id=store_id)
    startWaiting = waiting_models.StartWaiting.objects.get(store_id=store_id)
    photo_list = models.Image.objects.filter(store_id=store_id)

    if request.method == 'POST':
        store_form = forms.CreateStoreForm(request.POST)
        startWaiting_form = waiting_forms.StartWaitingForm(request.POST)

        if store_form.is_valid() and startWaiting_form.is_valid():

            store.name = store_form.cleaned_data['name']
            store.address = store_form.cleaned_data['address']
            store.store_type = store_form.cleaned_data['store_type']
            store.phone_number = store_form.cleaned_data['phone_number']
            store.food_type = store_form.cleaned_data['food_type']
            store.amenities.set(store_form.cleaned_data['amenities'])
            store.tags = store_form.cleaned_data['tags']
            store.save()

            images = request.FILES.getlist('file')
            if images:
                for image in images:
                    models.Image.objects.create(file=image, store=store)

            startWaiting.wait_time = startWaiting_form.cleaned_data['wait_time']
            startWaiting.table_number = startWaiting_form.cleaned_data['table_number']
            startWaiting.save()

            messages.success(request, "가게가 수정되었습니다")
            return redirect(reverse("users:my_list"))
    else:
        store_form = forms.CreateStoreForm()
        startWaiting_form = waiting_forms.StartWaitingForm()
        add_photo_form = forms.AddPhotoForm()
    print(store_form)
    store_form = forms.CreateStoreForm(instance=store)
    startWaiting_form = waiting_forms.StartWaitingForm(instance=startWaiting)
    add_photo_form = forms.AddPhotoForm()

    context = {
        "store_form": store_form,
        "startWaiting_form": startWaiting_form,
        "add_photo_form": add_photo_form,
        "photo_list": photo_list,
        "store": store,
    }
    return render(request, "stores/stores_modify.html", context)


def createQRcode(store):
    url = f"http://192.168.0.5:8000/stores/{store.id}/detail/"
    qrcode_img = qrcode.make(url)
    canvas = Image.new("RGB", (500, 500), "white")
    draw = ImageDraw.Draw(canvas)
    canvas.paste(qrcode_img)
    buffer = BytesIO()
    canvas.save(buffer, "PNG")
    store.qrcode.save(f'{store.name}-{store.id}.png', File(buffer))
    canvas.close()


@login_required
def createStore(request):

    current_user_id = request.user.id

    if request.method == 'POST':
        store_form = forms.CreateStoreForm(request.POST)
        startWaiting_form = waiting_forms.StartWaitingForm(request.POST)
        if store_form.is_valid() and startWaiting_form.is_valid():

            store = store_form.save(commit=False)
            store.user = request.user

            store.save()

            createQRcode(store)

            images = request.FILES.getlist('file')
            if images:
                for image in images:
                    models.Image.objects.create(file=image, store=store)

            startWaiting = startWaiting_form.save(commit=False)
            startWaiting.store_id = store.id
            startWaiting.master_id = current_user_id
            startWaiting.save()

            messages.success(request, "가게가 생성되었습니다")
            return redirect(reverse("stores:detail", kwargs={"store_id": store.id}))
    else:
        store_form = forms.CreateStoreForm()
        startWaiting_form = waiting_forms.StartWaitingForm()
        add_photo_form = forms.AddPhotoForm()

    context = {
        "store_form": store_form,
        "current_user_id": current_user_id,
        "add_photo_form": add_photo_form,
        "startWaiting_form": startWaiting_form,
    }
    return render(request, "stores/stores_create.html", context)


def deletePhoto(request, photo_id, store_id):

    photo = models.Image.objects.get(id=photo_id)
    photo.delete()

    return redirect(reverse("stores:modify", kwargs={"store_id": store_id}))
