from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponse

from .forms import AccountForm


def login(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        form_account = AccountForm(request.POST, request.FILES)
        if form.is_valid() and form_account.is_valid():
            form.save()
            form_account.save()
            return HttpResponse("User created success")
    return HttpResponse("")