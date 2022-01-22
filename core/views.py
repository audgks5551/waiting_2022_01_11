import os
from django.shortcuts import render

from stores import models as stores_models
from stores import forms as stores_forms


# def geocoding(address):
#    geolocoder = Nominatim(user_agent='South Korea')
#    geo = geolocoder.geocode(address)
#    crd = (geo.latitude, geo.longitude)
#    return crd


def home(request):

    NAVER_ID = os.environ.get("NAVER_ID")

    current_user_id = request.user.id

    store_list = stores_models.Store.objects.all()
    storeType_list = stores_models.StoreType.objects.all()
    amenity_list = stores_models.Amenity.objects.all()
    theme_list = stores_models.Theme.objects.all()
    taste_list = stores_models.Taste.objects.all()

    storeType_len = len(storeType_list)
    amenity_len = len(amenity_list)
    theme_len = len(theme_list)
    taste_len = len(taste_list)

    search_form = stores_forms.SearchForm()

    context = {
        "store_list": store_list,
        "current_user_id": current_user_id,
        "NAVER_ID": NAVER_ID,
        "storeType_list": storeType_list,
        "amenity_list": amenity_list,
        "theme_list": theme_list,
        "taste_list": taste_list,
        "storeType_len": storeType_len,
        "amenity_len": amenity_len,
        "theme_len": theme_len,
        "taste_len": taste_len,
        "search_form": search_form,
    }
    return render(request, "core/home_list.html", context)
