from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import FormMixin

from question_and_answer.forms import QuestionForm, AnswerForm
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


class DetailQuestion(DetailView, FormMixin):
    model = Question
    form_class = AnswerForm
    http_method_names = ['get', 'post']

    def post(self, request, pk):
        form_answer = self.form_class(request.POST)
        if form_answer.is_valid():
            answer = form_answer.save(commit=False)
            answer.author = request.user
            answer.question = Question.objects.get(pk=pk)
            answer.save()
            messages.success(self.request, 'Answer saved successfully')
            return redirect(answer.question.get_absolute_url())
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ChangeVotesClass(LoginRequiredMixin, View):
    http_method_names = ['get', ]

    def toggle_votes(self, selected_list_voted, another_list_voted):
        if self.request.user in selected_list_voted.all():
            selected_list_voted.remove(self.request.user)
            return
        selected_list_voted.add(self.request.user)
        if self.request.user in another_list_voted.all():
            another_list_voted.remove(self.request.user)

    def get(self, request, pk, votes_do):
        question = Question.objects.get(pk=pk)
        handler = {"up": (question.votes_up, question.votes_down), "down": (question.votes_down, question.votes_up)}
        self.toggle_votes(*handler[votes_do])
        return render(request, 'question_and_answer/question_detail.html', {"question": question})
