from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')
