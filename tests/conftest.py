import datetime
from base64 import b64encode
from datetime import timedelta

import pytest
from django.contrib.auth.models import User

from question_and_answer.models import Question, Answer, Tags


@pytest.fixture
def user():
    user = User.objects.create_user('username', password='very_Strong_password!@# Z', email="testemail@emai.com")
    yield user
    user.delete()


@pytest.fixture()
def authenticated_client(db, user):
    from django.test.client import Client

    client = Client()
    client.login(username=user.username, password="very_Strong_password!@# Z")
    return client


@pytest.fixture()
def tag(db):
    tag = Tags.objects.create(label='first label')
    yield tag
    tag.delete()


@pytest.fixture()
def question(db, user, tag):
    question = Question.objects.create(title="Title", text="Text question", author=user)
    question.tags.add(tag)
    yield question
    question.delete()


@pytest.fixture()
def answers(db, user, question):
    answers = [Answer.objects.create(text='This answer 1', question=question, author=user),
               Answer.objects.create(text='This answer 2', question=question, author=user),
               Answer.objects.create(text='This answer 3', question=question, author=user),
               Answer.objects.create(text='This answer 4', question=question, author=user)]
    return answers


@pytest.fixture()
def answers_two_page(db, user, question):
    for num in range(35):
        Answer.objects.create(text=f'This answer {num}', question=question, author=user)


@pytest.fixture()
def question_30(db, user):

    q = []
    for num in range(30):
        create_date = datetime.datetime.now() - timedelta(days=100 - num)
        q.append(Question.objects.create(title=f"This unique {num} question",
                                         text=b64encode(f'This unique text {num}'.encode()),
                                         author=user, date=create_date
                                         ))
    return q
