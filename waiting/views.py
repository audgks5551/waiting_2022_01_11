from django.shortcuts import render

def createWaiting(request):

    context = {}
    return render(request, "waiting/waiting_create.html", context)
