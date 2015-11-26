from django.shortcuts import render, redirect
from django.http import HttpResponse
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
            # Redirect to a success page.
            user_prof = UserProfile.objects.get(user=user)
            if user_prof.user_type is 0:
                return redirect("/ots/client/home/")
            elif user_prof.user_type is 1:
                return render(request, 'otsapp/trader_home.html')
            else: return render(request, 'otsapp/manager_home.html')
        else:
            return HttpResponse(json.dumps({"success":False}),
                                content_type="application/json")

def client_home(request):
    if request.method == "GET":
        print "1111111111111111"
        return render(request, 'otsapp/client_home.html')

