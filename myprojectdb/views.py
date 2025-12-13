from django.shortcuts import render, redirect
from django.http import HttpResponse 

def index(request):
    return render(request, 'index.html' )

def login_success(request):
    response = redirect("dashboard")
    response.set_cookie("logged_in", True, max_age=3600)
    return response

def dashboard(request):
    return render(request, "dashboard.html")


def handler404(request, exception):
    return render(request, '404.html', status=404)
