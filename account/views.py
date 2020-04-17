from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponse

from .forms import AccountForm
from .models import Account


def login(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        form_account = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if form_account.is_valid():
                account = form_account.save(commit=False)
                account.save()
                account.user = user
            else:
                account = Account.objects.create(user=user)
            messages.add_message(request, messages.INFO, 'You success sign up')
            return render(request, 'index.html')
    return HttpResponse("")
