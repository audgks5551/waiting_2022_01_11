from django.shortcuts import render

def createWaiting(request):

    current_user_id = request.user.id

    context = {"current_user_id": current_user_id}
    return render(request, "waiting/waiting_create.html", context)
