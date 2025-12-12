from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login-success/", views.login_success, name="login_success"),
    path("dashboard/", views.dashboard, name="dashboard"),
]

