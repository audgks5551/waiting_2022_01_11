from django.shortcuts import redirect, render, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#
from stores import models as stores_models
from waiting import models as waiting_models
from . import forms

@login_required
def listWaiting(request):

    current_user_id = request.user.id
    startWaiting_list = waiting_models.StartWaiting.objects.filter(master_id=current_user_id)
    store_list = stores_models.Store.objects.filter(user_id=current_user_id)
    print(startWaiting_list)
    print(store_list)
    get_store_minus_start = []
    for store in store_list:
        for startWaiting in startWaiting_list:
            if store.id == startWaiting.store.id:
                get_store_minus_start.append(store)
    
    print(get_store_minus_start)



    context = {
        "current_user_id": current_user_id,
        "store_list": store_list,
        "startWaiting_list": startWaiting_list
    }
    return render(request, "waiting/waiting_list.html", context)

@login_required
def createWaiting(request, store_id):
    current_user_id = request.user.id

    if request.method == "POST":
        form = forms.StartWaitingForm(request.POST)
        print(form)
        store = stores_models.Store.objects.get_or_none(id=store_id)
        if not store:
            return redirect(reverse("core:home"))
        if form.is_valid():
            startWaiting = form.save(commit=False)
            startWaiting.store_id = store.id
            startWaiting.master_id = current_user_id
            startWaiting.save()
            messages.success(request, "기달이 생성되었습니다")
            return redirect(reverse("waiting:detail", kwargs={"startWaiting_id": startWaiting.id}))
    else:
        form = forms.StartWaitingForm()
    
    context = {"current_user_id": current_user_id, "form": form, "store_id": store_id}
    return render(request, "waiting/waiting_create.html", context)

@login_required
def detailWaiting(request, startWaiting_id):

    current_user_id = request.user.id
    
    context = {"current_user_id": current_user_id, "startWaiting_id": startWaiting_id}
    return render(request, "waiting/waiting_detail.html", context)




