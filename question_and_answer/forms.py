from django import forms
from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)