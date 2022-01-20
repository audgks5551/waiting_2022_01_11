import os
from django.shortcuts import render

from stores import models as stores_models

from geopy.geocoders import Nominatim
import osmnx as ox


def geocoding(address):
    geolocoder = Nominatim(user_agent='South Korea')
    geo = geolocoder.geocode(address)
    crd = (geo.latitude, geo.longitude)
    return crd


def home(request):

    NAVER_ID = os.environ.get("NAVER_ID")

    current_user_id = request.user.id

    address_list = ['서울대입구역',
                    '도림로 264',
                    '현충로 213']

    demo = dict()
    for i in address_list:
        print(i)
        crd = geocoding(i)
        demo[i] = crd

    hi = demo["서울대입구역"]

    store_list = stores_models.Store.objects.all()

    context = {
        "store_list": store_list,
        "current_user_id": current_user_id,
        "NAVER_ID": NAVER_ID,
        "hi": hi,
    }
    return render(request, "core/home_list.html", context)
