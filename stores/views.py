from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required

#
import qrcode
from . import models

def storeList(request):

    store_list = models.Store.objects.all()
    
    context = {"store_list": store_list}
    return render(request, "stores/stores_list.html", context)

@login_required
def storeCreate(request):
    
    img = qrcode.make("https://google.com")
    img.save("static/qrcode/1.png")
    
    return redirect(reverse("stores:list"))