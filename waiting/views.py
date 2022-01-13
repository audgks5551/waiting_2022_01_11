from django.shortcuts import render

#
from stores import models as stores_models


def listWaiting(request):

    current_user_id = request.user.id
    store_list = stores_models.Store.objects.filter(user_id=current_user_id)

    context = {
        "current_user_id": current_user_id,
        "store_list": store_list
    }
    return render(request, "waiting/waiting_list.html", context)

def createWaiting(request, store_id):

    current_user_id = request.user.id

    context = {"current_user_id": current_user_id}
    return render(request, "waiting/waiting_create.html", context)

def detailWaiting(request, store_id):

    current_user_id = request.user.id
    
    context = {"current_user_id": current_user_id}
    return render(request, "waiting/waiting_detail.html", context)




