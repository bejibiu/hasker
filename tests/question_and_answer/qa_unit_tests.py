from django.contrib.auth.models import User
from django.urls import reverse

from question_and_answer.models import Question, Tags, Answer


def test_home_page_content_logo(client, db):
    res = client.get("/")
    content = res.content.decode()
    assert "logo" in content


def test_home_page_content_search(client, db):
    res = client.get("/")
    content = res.content.decode()
    assert "search" in content


def test_home_page_content_user_block(client, db):
    res = client.get("/")
    content = res.content.decode()
    assert "user_block" in content


def test_home_page_content_login(client, db):
    res = client.get("/")
    content = res.content.decode()
    assert "login" in content


def test_home_page_content_sign_up(client, db):
    res = client.get("/")
    content = res.content.decode()
    assert "sign_up" in content


def test_home_page_content_list_question(client, db):
    res = client.get("/")
    content = res.content.decode()
    assert "list_question" in content


def test_home_page_content_trending(client, db):
    res = client.get("/")
    content = res.content.decode()
    assert "trending" in content


def test_home_page_content_popular_questions(client, db):
    res = client.get("/")
    content = res.content.decode()
    assert "popular_questions" in res.context_data.keys()


class TestQuestionCase:
    def test_popular_max_20_question(self, client, db, question_30):
        res = client.get("/")
        popular_question = res.context_data["popular_questions"]
        assert len(popular_question) == 20

    def test_fail_ask_not_auth_client(self, client):
        data = {"title": "Title for message", "question": "is that a question?"}
        res = client.post(reverse("save_question"), data)
        assert res.status_code == 200

    def test_save_question_without_tags(self, authenticated_client):
        data = {"title": "Title for message", "text": "is that a question?", "tags": ""}
        authenticated_client.post(reverse("save_question"), data)
        assert Question.objects.first().title == data["title"]

    def test_save_question_with_tags(self, authenticated_client):
        data = {"title": "Title for message", "text": "is that a question?", "tags": "1,2"}
        res = authenticated_client.post(reverse("save_question"), data)
        question = Question.objects.first()
        assert res.status_code == 302
        assert Question.objects.all().count() == 1
        assert Question.objects.first().title == data["title"]
        assert Tags.objects.count() == 2
        assert question.votes == 0
        assert question.answer_count == 0

    def test_save_question_with_max_3tags(self, authenticated_client):
        data = {
            "title": "Title for message",
            "text": "is that a question?",
            "tags": "1,2,3,4",
        }
        res = authenticated_client.post(reverse("save_question"), data)
        assert Tags.objects.count() == 3

    def test_upper_votes(self, authenticated_client, question):
        res = authenticated_client.get(f"{question.get_absolute_url()}up/")
        assert question.votes == 1
        res = authenticated_client.get(f"{question.get_absolute_url()}up/")
        assert question.votes == 0

    def test_downer_votes(self, authenticated_client, question):
        res = authenticated_client.get(f"{question.get_absolute_url()}down/")
        assert question.votes == -1
        res = authenticated_client.get(f"{question.get_absolute_url()}down/")
        assert question.votes == 0

    def test_toggle_votes(self, authenticated_client, question):
        authenticated_client.get(f"{question.get_absolute_url()}up/")
        assert question.votes == 1
        authenticated_client.get(f"{question.get_absolute_url()}down/")
        assert question.votes == -1


class TestAnswer:
    def test_upper_votes_to_answer(self, authenticated_client, answers):
        answer = answers[0]
        res = authenticated_client.get(f"{answer.get_absolute_url()}up/")
        assert answer.votes == 1
        res = authenticated_client.get(f"{answer.get_absolute_url()}up/")
        assert answer.votes == 0

    def test_set_answer_as_correct(self, authenticated_client, answers):
        answer = answers[0]
        authenticated_client.get(answer.get_absolute_url_to_toggle_answer_as_correct())
        assert Answer.objects.get(pk=answer.pk).correct

    def test_set_answer_as_correct_if_not_author(self, authenticated_client, answers):
        answer = answers[0]
        user = User.objects.create(username="new_user")
        answer.question.author = user
        answer.question.save()
        res = authenticated_client.get(
            answer.get_absolute_url_to_toggle_answer_as_correct()
        )
        assert not answer.correct
        assert res.status_code == 403

    def test_toggle_answer_correct(self, authenticated_client, answers):
        answer = answers[0]
        authenticated_client.get(answer.get_absolute_url_to_toggle_answer_as_correct())
        assert Answer.objects.get(pk=answer.id).correct
        authenticated_client.get(answer.get_absolute_url_to_toggle_answer_as_correct())
        assert Answer.objects.get(pk=answer.id).correct is False

    def test_toggle_answer_correct_after_set_another_answer_correct(self, authenticated_client, answers):
        answer1 = answers[1]
        answer2 = answers[2]
        authenticated_client.get(answer1.get_absolute_url_to_toggle_answer_as_correct())
        assert Answer.objects.get(pk=answer1.id).correct
        authenticated_client.get(answer2.get_absolute_url_to_toggle_answer_as_correct())
        assert Answer.objects.get(pk=answer1.id).correct is False


class TestSearch:
    def test_tags_search(self, client, question):
        res = client.get(
            reverse("search_question"), {"q": f"tag:{question.tags.first().label}"}
        )
        assert res.context_data["object_list"].first() == question
