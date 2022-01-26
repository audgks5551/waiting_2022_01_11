from django.http import JsonResponse
import json
import os
from django.shortcuts import redirect, render, reverse

from stores import models as stores_models
from stores import forms as stores_forms
from stores import search
from django.core.paginator import Paginator

# def geocoding(address):
#    geolocoder = Nominatim(user_agent='South Korea')
#    geo = geolocoder.geocode(address)
#    crd = (geo.latitude, geo.longitude)
#    return crd


def home(request):

    NAVER_ID = os.environ.get("NAVER_ID")

    current_user_id = request.user.id

    storeType_len = stores_models.StoreType.objects.count()
    amenity_len = stores_models.Amenity.objects.count()
    theme_len = stores_models.Theme.objects.count()
    taste_len = stores_models.Taste.objects.count()

    queryset = stores_models.Store.objects.all()
    paginator = Paginator(queryset, 50, orphans=5)

    page = request.GET.get("page", 1)

    store_list = paginator.get_page(page)

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


def getCompletion(request):
    keyword = request.GET["keyword"]

    name_list = search.elasticsearch_completion(keyword)

    data = []
    for name in name_list:
        data.append({
            "name": name
        })

    return JsonResponse(data, safe=False)
