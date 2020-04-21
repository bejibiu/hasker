from django.urls import reverse

from question_and_answer.models import Question, Tags


def test_home_page_content(client):
    res = client.get('/')
    elements_by_id_on_home_page = [
        'logo',
        'search',
        'user_block',
        'login',
        'sign_up',
        'list_question',
        'trending'
    ]

    res = res.content.decode()

    for element in elements_by_id_on_home_page:
        assert element in res


def test_fail_ask_not_auth_client(client):
    data = {"title": "Title for message", "question": "is that a question?"}
    res = client.post(reverse('save_question'), data)
    assert res.status_code == 200


def test_save_question_without_tags(authenticated_client):
    data = {"title": "Title for message", "text": "is that a question?", "tags":""}
    res = authenticated_client.post(reverse("save_question"), data)
    assert Question.objects.all().count() == 1
    assert Question.objects.first().title == data["title"]
    assert res.status_code == 302


def test_save_question_with_tags(authenticated_client):
    data = {"title": "Title for message", "text": "is that a question?", "tags": "1,2"}
    res = authenticated_client.post(reverse("save_question"), data)
    assert Question.objects.all().count() == 1
    assert Question.objects.first().title == data["title"]
    assert Tags.objects.count() == 2
    assert res.status_code == 302
