from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import resolve
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
    assert Account.objects.all().count() == 1
    assert Account.objects.first().avatar

