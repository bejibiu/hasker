import logging

from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, CreateView

from .forms import AccountForm, UserChangeFormSimple, RegistrationUser
from .models import Account


class CreateUserWithAvatar(CreateView):
    form_class = RegistrationUser
    template_name = 'index.html'

    def form_valid(self, form):
        user = form.save()
        logging.info(f"create user with email={user.email}")
        form_account = AccountForm(self.request.POST, self.request.FILES, instance=user.account)
        if form_account.is_valid():
            account = form_account.save(commit=False)
            account.user = user
            account.save()
            logging.info(f'create avatar to user {user.email}')
        else:
            Account.objects.create(user=user)
        auth.login(self.request, user)
        messages.add_message(self.request, messages.SUCCESS, 'You success sign up')
        return redirect('/')


class SettingsUpdate(LoginRequiredMixin, UpdateView):
    form_class = AccountForm
    template_name = 'account/settings.html'

    def get_object(self, queryset=None):
        return self.request.user.account

    def post(self, request, *args, **kwargs):
        user_form = UserChangeFormSimple(request.POST, instance=request.user)
        account_form = AccountForm(request.POST, request.FILES, instance=request.user.account)
        if user_form.is_valid() and account_form.is_valid():
            new_email = user_form.cleaned_data['email']
            logging.info(f"user {request.user} change email from {request.user.email} to {new_email}")
            user_form.save()
            account = account_form.save(commit=False)
            account.user = request.user
            account_form.save()
            messages.add_message(request, messages.SUCCESS, 'Success update')
        return render(request, 'account/settings.html', {"user_form": user_form, "form": account_form})

    def get_context_data(self, **kwargs):
        kwargs["user_form"] = UserChangeFormSimple(initial={"username": self.request.user.username,
                                                            "email": self.request.user.email})
        return super(SettingsUpdate, self).get_context_data(**kwargs)


class LoginAccountView(LoginView):
    template_name = 'account/login.html'

    def get_success_url(self):
        if f'?{self.redirect_field_name}=' in self.request.META.get('HTTP_REFERER', ""):
            return self.request.META.get('HTTP_REFERER').split(f'?{self.redirect_field_name}=')[-1]
        redirect = super(LoginAccountView, self).get_success_url()
        return redirect
