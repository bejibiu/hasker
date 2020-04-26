from django import forms
from .models import Question, Answer, Tags


class MultiTagField(forms.Field):
    def to_python(self, value):
        if not value:
            return []
        return value.strip().split(',')[:3]


class QuestionForm(forms.ModelForm):
    tags = MultiTagField(required=False)

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)
