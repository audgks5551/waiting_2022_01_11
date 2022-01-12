from django.shortcuts import render

from stores import models as stores_models
def home(request):
    
    current_user_id = request.user.id

    store_list = stores_models.Store.objects.all()
    
    context = {"store_list": store_list, "current_user_id": current_user_id}
    return render(request, "core/home_list.html", context)
