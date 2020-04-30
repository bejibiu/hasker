from django import forms
from django.contrib.auth.forms import UserChangeForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User

from .models import Account


class AccountForm(forms.ModelForm):
    avatar = forms.FileField(required=False)

    class Meta:
        model = Account
        fields = 'avatar',


class UserChangeFormSimple(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
        self.fields['username'].widget.attrs.update({'readonly': 'readonly'})


class RegistrationUser(UserCreationForm):
    avatar = forms.FileField(required=False)