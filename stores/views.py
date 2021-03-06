
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse
from django.views.generic import View
from django.core.paginator import Paginator

# qrcode
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File

#
from . import models
from . import forms
from . import search
from waiting import forms as waiting_forms
from waiting import models as waiting_models


class SearchView(View):

    """ 검색 """

    def get(self, request):

        current_user_id = request.user.id

        storeType_len = models.StoreType.objects.count()
        amenity_len = models.Amenity.objects.count()
        theme_len = models.Theme.objects.count()
        taste_len = models.Taste.objects.count()

        keyword = request.GET.get("keyword")

        if keyword:

            form = forms.SearchForm(request.GET)

            if form.is_valid():

                #store_types = form.cleaned_data.get("store_type")
                amenities = form.cleaned_data.get("amenities", "")
                themes = form.cleaned_data.get("themes", "")
                tastes = form.cleaned_data.get("tastes", "")

                #store_type_list = []
                # for store_type in store_types:
                #    store_type_list.append(store_type.name)
                amenity_list = []
                for amenity in amenities:
                    amenity_list.append(amenity.name)
                theme_list = []
                for theme in themes:
                    theme_list.append(theme.name)
                taste_list = []
                for taste in tastes:
                    taste_list.append(taste.name)

                queryset, em_list = search.elasticsearch_search(
                    keyword, amenity_list, theme_list, taste_list)

                paginator = Paginator(queryset, 30, orphans=5)

                page = request.GET.get("page", 1)

                store_list = paginator.get_page(page)

                return render(
                    request, "stores/stores_list.html", {
                        "search_form": form,
                        "store_list": store_list,
                        "current_user_id": current_user_id,
                        "storeType_len": storeType_len,
                        "amenity_len": amenity_len,
                        "theme_len": theme_len,
                        "taste_len": taste_len
                    }
                )

        else:
            search_form = forms.SearchForm()

        return render(request, "stores/stores_list.html", {
            "search_form": search_form,
            "current_user_id": current_user_id,
            "storeType_len": storeType_len,
            "amenity_len": amenity_len,
            "theme_len": theme_len,
            "taste_len": taste_len
        })


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

    search_form = forms.SearchForm()

    context = {
        "store": store,
        "current_user_id": current_user_id,
        "store_id": store_id,
        "waiting_mode": waiting_mode,
        "search_form": search_form
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
        search_form = forms.SearchForm()

    store_form = forms.CreateStoreForm(instance=store)
    startWaiting_form = waiting_forms.StartWaitingForm(instance=startWaiting)
    add_photo_form = forms.AddPhotoForm()

    context = {
        "store_form": store_form,
        "startWaiting_form": startWaiting_form,
        "add_photo_form": add_photo_form,
        "search_form": search_form,
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
        search_form = forms.SearchForm()

    storeType_len = models.StoreType.objects.count()
    amenity_len = models.Amenity.objects.count()
    theme_len = models.Theme.objects.count()
    taste_len = models.Taste.objects.count()

    context = {
        "store_form": store_form,
        "current_user_id": current_user_id,
        "add_photo_form": add_photo_form,
        "startWaiting_form": startWaiting_form,
        "search_form": search_form,
        "storeType_len": storeType_len,
        "amenity_len": amenity_len,
        "theme_len": theme_len,
        "taste_len": taste_len,
    }
    return render(request, "stores/stores_create.html", context)


def deletePhoto(request, photo_id, store_id):

    photo = models.Image.objects.get(id=photo_id)
    photo.delete()

    return redirect(reverse("stores:modify", kwargs={"store_id": store_id}))
