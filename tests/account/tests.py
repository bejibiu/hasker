from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import resolve
from django.contrib.auth.models import User
import pytest

from account.models import Account


@pytest.fixture
def path_to_login():
    return "/account/login/"


@pytest.fixture
def avatar():
    return SimpleUploadedFile("avatar.png", b"png...", content_type="image/png")


def test_return_correct_resolve_path(path_to_login):
    func = resolve(path_to_login)
    assert func.view_name == 'account.views.login'


@pytest.mark.django_db
def test_create_user_account_with_post(client, path_to_login, avatar):
    data = {
        "email": "test@mail.com",
        "username": "test",
        "password1": "superPassword123",
        "password2": "superPassword123",
        "avatar": avatar
    }

    client.post(path_to_login, data=data)
    user = User.objects.select_related('account').first

    assert User.objects.count() == 1
    assert user.account.avatar.name


@pytest.mark.django_db
def test_create_user_account_with_post(client, path_to_login):
    data = {
        "email": "test@mail.com",
        "username": "test",
        "password1": "superPassword123",
        "password2": "superPassword123",
    }

    client.post(path_to_login, data=data)
    user = User.objects.select_related('account').first()
    assert User.objects.count() == 1
    assert not user.account.avatar.name

