import pytest
from django.contrib.auth.models import User

from question_and_answer.models import Question, Answer


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


@pytest.fixture()
def answers(db, user, question):
    answers = [Answer.objects.create(text='This answer 1', question=question, author=user),
               Answer.objects.create(text='This answer 2', question=question, author=user),
               Answer.objects.create(text='This answer 3', question=question, author=user),
               Answer.objects.create(text='This answer 4', question=question, author=user)]
    return answers

