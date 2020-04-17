from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import resolve, reverse
from django.contrib.auth.models import User
import pytest


@pytest.fixture
def avatar():
    return SimpleUploadedFile("avatar.png", b"png...", content_type="image/png")


def test_return_correct_resolve_path_registration():
    func = resolve("/account/registration/")
    assert func.view_name == 'registration'


@pytest.mark.django_db
def test_create_user_account_with_post(client, avatar):
    data = {
        "email": "test@mail.com",
        "username": "test",
        "password1": "superPassword123",
        "password2": "superPassword123",
        "avatar": avatar
    }

    client.post(reverse('registration'), data=data)
    user = User.objects.select_related('account').first

    assert User.objects.count() == 1
    assert user.account.avatar.name


@pytest.mark.django_db
def test_create_user_account_with_post(client):
    data = {
        "email": "test@mail.com",
        "username": "test",
        "password1": "superPassword123",
        "password2": "superPassword123",
    }

    client.post(reverse('registration'), data=data)
    user = User.objects.select_related('account').first()
    assert User.objects.count() == 1
    assert not user.account.avatar.name


@pytest.mark.django_db
def test_login_with_post(client, user):
    data = {
        "username": f"{user.username}",
        "password": "very_Strong_password!@# Z",
    }

    res = client.post(reverse('login'), data=data)

    assert res.status_code == 302
