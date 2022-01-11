from django.shortcuts import redirect, render, reverse

#
import qrcode

def storeList(request):

    context = {}
    return render(request, "stores/stores_list.html", context)

def storeCreate(request):

    img = qrcode.make("https://google.com")
    img.save("static/qrcode/1.png")
    
    return redirect(reverse("stores:list"))