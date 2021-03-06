from django.shortcuts import redirect, render, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#
from stores import models as stores_models
from . import models as waiting_models
from . import forms


@login_required(login_url='/users/login')
def listWaiting(request):

    current_user_id = request.user.id
    startWaiting_list = waiting_models.StartWaiting.objects.filter(
        master_id=current_user_id)

    context = {
        "current_user_id": current_user_id,
        "startWaiting_list": startWaiting_list
    }
    return render(request, "waiting/waiting_list.html", context)


@login_required(login_url='/users/login')
def detailWaiting(request, startWaiting_id):

    current_user_id = request.user.id

    waiting_list = waiting_models.Waiting.objects.filter(
        startWaiting_id=startWaiting_id)
    context = {"current_user_id": current_user_id,
               "startWaiting_id": startWaiting_id,
               "waiting_list": waiting_list}
    return render(request, "waiting/waiting_detail.html", context)


@login_required(login_url='/users/login')
def addUser(request, store_id):

    current_user_id = request.user.id
    startWaiting = waiting_models.StartWaiting.objects.get(store_id=store_id)

    if request.method == "POST":
        form = forms.WaitingForm(request.POST)
        print(form)
        if form.is_valid():
            Waiting = form.save(commit=False)
            Waiting.startWaiting_id = startWaiting.id
            Waiting.number = startWaiting.number
            startWaiting.number += 1
            startWaiting.save()
            Waiting.user_id = current_user_id
            Waiting.time = startWaiting.wait_time * startWaiting.waitings.count()
            Waiting.save()
            messages.success(request, f"기달 고고 대기번호:{Waiting.number}")
            return redirect(reverse("stores:detail", kwargs={"store_id": store_id}))

    form = forms.WaitingForm()

    context = {"current_user_id": current_user_id, "form": form}
    return render(request, "waiting/waiting_add.html", context)

@login_required(login_url='/users/login')
def removeUser(request, waiting_id):
    waiting_user = waiting_models.Waiting.objects.get(id=waiting_id)
    startWaiting_id = waiting_user.startWaiting_id
    waiting_user.delete()
    return redirect(reverse("waiting:detail", kwargs={"startWaiting_id": startWaiting_id}))


@login_required(login_url='/users/login')
def startMode(request, startWaiting_id):
    startWaiting = waiting_models.StartWaiting.objects.get(id=startWaiting_id)
    startWaiting.mode = True
    startWaiting.save()
    return redirect(reverse("waiting:detail", kwargs={"startWaiting_id": startWaiting_id}))


@login_required(login_url='/users/login')
def stopMode(request, startWaiting_id):
    startWaiting = waiting_models.StartWaiting.objects.get(id=startWaiting_id)
    startWaiting.mode = False
    startWaiting.save()
    return redirect(reverse("waiting:detail", kwargs={"startWaiting_id": startWaiting_id}))


@login_required(login_url='/users/login')
def resetMode(request, startWaiting_id):
    waiting_list = waiting_models.Waiting.objects.filter(
        startWaiting_id=startWaiting_id)
    for waiting in waiting_list:
        waiting.delete()
    return redirect(reverse("waiting:detail", kwargs={"startWaiting_id": startWaiting_id}))
