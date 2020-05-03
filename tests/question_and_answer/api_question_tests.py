import pytest


@pytest.fixture()
def api_question_path():
    return '/api/v1/questions/'


class TestQuestionApi:
    def test_paginate_question_api(self, question_30, rest_client, api_question_path):
        res = rest_client.get(api_question_path)
        assert len(res.data['results']) == 20

    def test_search_question_with_title(self, rest_client, question, api_question_path):
        res = rest_client.get(api_question_path + f"?search={question.title}")
        assert res.data['count'] == 1

    def test_search_question_with_text(self, rest_client, question, api_question_path):
        res = rest_client.get(api_question_path + f"?search={question.text}")
        assert res.data['count'] == 1

    def test_search_question_not_exist_title(self, rest_client, question, api_question_path):
        res = rest_client.get(api_question_path + f"?search={question.title}+Notexists")
        assert res.data['count'] == 0


class TestAnswerApiCase:
    def test_all_answer_by_question(self, rest_client, answers, api_question_path):
        question_id = answers[0].question.id

        res = rest_client.get(api_question_path + f'{question_id}/answers/')
        assert len(res.data) == len(answers)
