import pytest
from django.contrib.auth.models import User

from question_and_answer.models import Question


@pytest.fixture
def user():
    user = User.objects.create_user('username', password='very_Strong_password!@# Z')
    yield user
    user.delete()


@pytest.fixture()
def authenticated_client(db, user):
    from django.test.client import Client

    client = Client()
    client.login(username=user.username, password="very_Strong_password!@# Z")
    return client


@pytest.fixture()
def question(db, user):
    question = Question.objects.create(title="Title", text="Text question", author=user)
    yield question
    question.delete()
