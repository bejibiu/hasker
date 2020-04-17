from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path("registration/", views.registration, name="registration"),
    path("login", LoginView.as_view(), name="login")
]
