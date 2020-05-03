from rest_framework import serializers

from question_and_answer.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["text", "author", "date", "title", "tags", ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['votes'] = instance.votes
        return ret


class PopularQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["title"]
        # fields = ["text", "author", "date", "title", "tags", ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['votes'] = instance.votes
        return ret
