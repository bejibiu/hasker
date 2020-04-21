from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView

from question_and_answer.forms import QuestionForm
from question_and_answer.models import Question, Tags


class HomePageTemplate(ListView):
    model = Question
    template_name = 'index.html'


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm

    def post(self, request, *args, **kwargs):
        question_form = self.form_class(request.POST)

        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.author = request.user
            question.save()
            tags = question_form.data['tags']
            for tag in tags.split(',')[:question.max_tags]:
                question.tags.add(Tags.objects.create(label=tag))
            messages.success(self.request, 'Ask saved successfully')
            return redirect(reverse('home'))
        return render(request, "index.html", {"question_form": question_form})
