import logging

from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

from .forms import AccountForm
from .models import Account


def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        form_account = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            logging.info(f"create user with email={user.email}")
            if form_account.is_valid():
                account = form_account.save(commit=False)
                account.save()
                account.user = user
                logging.info(f'create avatar to user {user.email}')
            else:
                Account.objects.create(user=user)
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, 'You success sign up')
            return render(request, 'base.html')
    return render(request, 'base.html')
