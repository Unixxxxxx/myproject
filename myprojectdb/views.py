from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.template import RequestContext
from django.utils import timezone
from .forms import LoginForm
def index(request):
    return render(request, 'index.html' )

def login_success(request):
    response = redirect("dashboard")
    response.set_cookie("logged_in", True, max_age=3600)
    return response

def dashboard(request):
    username = request.COOKIES.get('username', 'Guest')
    last_connection = request.COOKIES.get('last_connection', 'Unknown')

    return render(request, 'dashboard.html', {
        'username': username,
        'last_connection': last_connection
    })


def handler404(request, exception):
    return render(request, '404.html', status=404)

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']

            # Create response FIRST
            response = render(
                request,
                'loggedin.html',
                {'username': username}
            )

            #  SET COOKIE HERE 👇
            response.set_cookie(
                'username',
                username,
                max_age=3600,
                httponly=True,
                secure=True,   # works only with HTTPS
                samesite='Lax'
            )

            response.set_cookie(
                'last_connection',
                timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                max_age=3600
            )

            #  Return response
            return response

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


