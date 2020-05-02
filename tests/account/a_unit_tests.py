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


def test_correct_resolve_account_settings():
    func = resolve('/account/settings/')
    assert func.view_name == 'account_settings'


class CreateAccountCase:
    @pytest.mark.django_db
    def test_create_user_account_with_avatar(self, client, avatar):
        data = {
            "email": "test@mail.com",
            "username": "test",
            "password1": "superPassword123",
            "password2": "superPassword123",
            "avatar": avatar
        }

        client.post(reverse('registration'), data=data)
        user = User.objects.select_related('account').first()

        assert User.objects.count() == 1
        assert user.account.avatar.name

    @pytest.mark.django_db
    def test_create_user_account_with_post(self, client):
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
    def test_login_with_post(self, client, user):
        data = {
            "username": f"{user.username}",
            "password": "very_Strong_password!@# Z",
        }

        res = client.post(reverse('login'), data=data)

        assert res.status_code == 302


class TestSettingsCase:
    def test_not_available_settings_page_not_auth(self, client):
        res = client.get(reverse('account_settings'))
        assert res.status_code == 302

    def test_available_settings_in_auth_client(self, authenticated_client):
        res = authenticated_client.get(reverse('account_settings'))
        assert res.status_code == 200

    def test_correct_template_for_settings(self, authenticated_client):
        res = authenticated_client.get(reverse('account_settings'))
        assert 'account/settings.html' in (t.name for t in res.templates)


def test_save_new_email(authenticated_client, user):
    new_email = "new-email@email.com"
    res = authenticated_client.post(reverse('account_settings'),
                                    {"email": new_email,
                                     "username": user.username})
    assert res.status_code == 200
    assert User.objects.all().first().email != user.email
    assert User.objects.all().first().email == new_email
