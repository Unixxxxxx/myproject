from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.template import RequestContext
from django.utils import timezone
from .forms import LoginForm
def index(request):
    return render(request, 'index.html' )

def login_success(request):
    # Use server-side session instead of setting a cookie
    request.session['logged_in'] = True
    request.session.modified = True
    return redirect("dashboard")

def dashboard(request):
    username = request.session.get('username', 'Guest')
    last_connection = request.session.get('last_connection', 'Unknown')

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
            # Store auth info server-side in the session instead of cookies
            request.session['username'] = username
            request.session['last_connection'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            request.session.modified = True

            #  Return response
            return response

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def session_login(request):
    """Session-based login helper: set session keys instead of cookies."""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            # If using Django authentication, call authenticate() here and set user id in session.
            request.session['username'] = username
            request.session['logged_in'] = True
            request.session['last_connection'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            request.session.modified = True
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def session_logout(request):
    """Clear session-based authentication."""
    request.session.pop('username', None)
    request.session.pop('logged_in', None)
    request.session.pop('last_connection', None)
    request.session.flush()
    return redirect('login')
