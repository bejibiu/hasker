from rest_framework import serializers

from question_and_answer.models import Question, Answer


class VotesMixin(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['votes'] = instance.votes
        return ret


class AnswerSerializer(VotesMixin):
    class Meta:
        model = Answer
        fields = ["text", "author", "date", "correct", ]


class QuestionSerializer(VotesMixin):
    class Meta:
        model = Question
        fields = ["text", "author", "date", "title", "tags", ]


class PopularQuestionSerializer(VotesMixin):
    class Meta:
        model = Question
        fields = ["title"]
