import logging

from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .forms import AccountForm, UserChangeFormSimple
from .models import Account


def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            logging.info(f"create user with email={user.email}")
            form_account = AccountForm(request.POST, request.FILES, instance=user.account)
            if form_account.is_valid():
                account = form_account.save(commit=False)
                account.user = user
                account.save()
                logging.info(f'create avatar to user {user.email}')
            else:
                Account.objects.create(user=user)
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, 'You success sign up')
            return render(request, 'index.html')
    return render(request, 'index.html')


@login_required
def settings(request):
    if request.method == "POST":
        user_form = UserChangeFormSimple(request.POST, instance=request.user)
        account_form = AccountForm(request.POST, request.FILES, instance=request.user.account)
        if user_form.is_valid() and account_form.is_valid():
            new_email = user_form.cleaned_data['email']
            logging.info(f"user {request.user} change email from {request.user.email } to {new_email}")
            user_form.save()
            account = account_form.save(commit=False)
            account.user = request.user
            account_form.save()
            messages.add_message(request, messages.SUCCESS, 'Success update')
        return render(request, 'account/settings.html', {"user_form": user_form, "form": account_form})
    user_form = UserChangeFormSimple(initial={"username": request.user.username, "email": request.user.email})
    account_form = AccountForm(initial={"user": request.user})
    return render(request, 'account/settings.html', {"user_form": user_form, "form": account_form})

