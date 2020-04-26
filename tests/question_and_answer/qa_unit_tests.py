from django.contrib.auth.models import User
from django.urls import reverse

from question_and_answer.models import Question, Tags, Answer


def test_home_page_content(client, db):
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
    data = {"title": "Title for message", "text": "is that a question?", "tags": ""}
    res = authenticated_client.post(reverse("save_question"), data)
    assert Question.objects.all().count() == 1
    assert Question.objects.first().title == data["title"]
    assert res.status_code == 302


def test_save_question_with_tags(authenticated_client):
    data = {"title": "Title for message", "text": "is that a question?", "tags": "1,2"}
    res = authenticated_client.post(reverse("save_question"), data)
    question = Question.objects.first()
    assert res.status_code == 302
    assert Question.objects.all().count() == 1
    assert Question.objects.first().title == data["title"]
    assert Tags.objects.count() == 2
    assert question.votes == 0
    assert question.answer_count == 0


def test_save_question_with_max_3tags(authenticated_client):
    data = {"title": "Title for message", "text": "is that a question?", "tags": "1,2,3,4"}
    res = authenticated_client.post(reverse("save_question"), data)
    assert Tags.objects.count() == 3


def test_upper_votes(authenticated_client, question):
    res = authenticated_client.get(f'{question.get_absolute_url()}up/')
    assert question.votes == 1
    res = authenticated_client.get(f'{question.get_absolute_url()}up/')
    assert question.votes == 0


def test_downer_votes(authenticated_client, question):
    res = authenticated_client.get(f'{question.get_absolute_url()}down/')
    assert question.votes == -1
    res = authenticated_client.get(f'{question.get_absolute_url()}down/')
    assert question.votes == 0


def test_toggle_votes(authenticated_client, question):
    authenticated_client.get(f'{question.get_absolute_url()}up/')
    assert question.votes == 1
    authenticated_client.get(f'{question.get_absolute_url()}down/')
    assert question.votes == -1


# answer toggle votes
def test_upper_votes_to_answer(authenticated_client, answers):
    answer = answers[0]
    res = authenticated_client.get(f'{answer.get_absolute_url()}up/')
    assert answer.votes == 1
    res = authenticated_client.get(f'{answer.get_absolute_url()}up/')
    assert answer.votes == 0


def test_set_answer_as_right(authenticated_client, answers):
    answer = answers[0]
    authenticated_client.get(answer.get_absolute_url_to_toggle_answer_as_right())
    assert Answer.objects.get(pk=answer.pk).right


def test_set_answer_as_right_if_not_author(authenticated_client, answers):
    answer = answers[0]
    user = User.objects.create(username='new_user')
    answer.question.author = user
    answer.question.save()
    res = authenticated_client.get(answer.get_absolute_url_to_toggle_answer_as_right())
    assert not answer.right
    assert res.status_code == 403


def test_toggle_answer_right(authenticated_client, answers):
    answer = answers[0]
    authenticated_client.get(answer.get_absolute_url_to_toggle_answer_as_right())
    assert Answer.objects.get(pk=answer.id).right
    authenticated_client.get(answer.get_absolute_url_to_toggle_answer_as_right())
    assert Answer.objects.get(pk=answer.id).right is False


def test_toggle_answer_right_after_set_another_answer_right(authenticated_client, answers):
    answer1 = answers[1]
    answer2 = answers[2]
    authenticated_client.get(answer1.get_absolute_url_to_toggle_answer_as_right())
    assert Answer.objects.get(pk=answer1.id).right
    authenticated_client.get(answer2.get_absolute_url_to_toggle_answer_as_right())
    assert Answer.objects.get(pk=answer1.id).right is False


def test_tags_search(client, question):
    res = client.get(reverse('search_question'), {"q": f"tag:{question.tags.first().label}"})
    assert res.context_data["object_list"].first() == question
