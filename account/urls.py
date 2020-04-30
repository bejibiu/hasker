from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import SettingsUpdate, CreateUserWithAvatar, LoginAccountView

urlpatterns = [
    path("registration/", CreateUserWithAvatar.as_view(), name="registration"),
    path("login/", LoginAccountView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('settings/', SettingsUpdate.as_view(), name='account_settings'),
]
