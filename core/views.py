from django.shortcuts import render

from stores import models as stores_models
def home(request):

    store_list = stores_models.Store.objects.all()
    
    context = {"store_list": store_list}
    return render(request, "core/home_list.html", context)
