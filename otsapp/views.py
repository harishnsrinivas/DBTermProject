from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return HttpResponse("Test index...")


def login(request):
    if request.method == "GET":
        return render(request, 'otsapp/loginview.html')
