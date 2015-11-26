from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

from otsapp.models import UserProfile



@login_required
def index(request):
    return HttpResponse("Test index...")


def login(request):
    if request.method == "GET":
        return render(request, 'otsapp/loginview.html')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,
            password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            return HttpResponse(json.dumps({"success":True}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"success":False}),
                                content_type="application/json")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/ots/")



def home_dashborad(request):
    if request.method == "GET":
        user = request.user
        user_prof = UserProfile.objects.get(user=user)
        if user_prof.user_type == 0:
            _template = "otsapp/client_home.html"
        elif user_prof.user_type == 1:
            _template = "otsapp/trader_home.html"
        else:
            _template = "otsapp/manager_home.html"

        return render(request, _template)

