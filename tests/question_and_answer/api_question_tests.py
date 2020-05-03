import pytest


@pytest.fixture()
def api_question_path():
    return '/api/v1/questions/'


class TestQuestionApi:
    def test_paginate_question_api(self, question_30, rest_client, api_question_path):
        res = rest_client.get(api_question_path)
        assert len(res.data['results']) == 20
