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
    storeType_len = stores_models.StoreType.objects.count()
    amenity_len = stores_models.Amenity.objects.count()
    theme_len = stores_models.Theme.objects.count()
    taste_len = stores_models.Taste.objects.count()

    search_form = stores_forms.SearchForm()

    context = {
        "store_list": store_list,
        "current_user_id": current_user_id,
        "NAVER_ID": NAVER_ID,
        "storeType_len": storeType_len,
        "amenity_len": amenity_len,
        "theme_len": theme_len,
        "taste_len": taste_len,
        "search_form": search_form,
    }
    return render(request, "core/home_list.html", context)
