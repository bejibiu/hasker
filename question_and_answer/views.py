from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import FormMixin

from question_and_answer.forms import QuestionForm, AnswerForm
from question_and_answer.models import Question, Tags, Answer


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
    login_url = '/account/login/'
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
        return redirect(reverse('detail_question', args=pk))


class ChangeVotesAnswerClass(LoginRequiredMixin, View):
    login_url = '/account/login/'
    http_method_names = ['get', ]

    def toggle_votes(self, pk_question, selected_list_voted, another_list_voted):
        if self.request.user in selected_list_voted.all():
            selected_list_voted.remove(self.request.user)
            return
        [answer.votes_down.remove(self.request.user) for answer in
         Answer.objects.filter(question_id=pk_question).filter(votes_down=self.request.user)]
        [answer.votes_up.remove(self.request.user) for answer in
         Answer.objects.filter(question_id=pk_question).filter(votes_up=self.request.user)]
        selected_list_voted.add(self.request.user)
        if self.request.user in another_list_voted.all():
            another_list_voted.remove(self.request.user)

    def get(self, request, pk_question, pk, votes_do):
        answer = Answer.objects.get(pk=pk)
        handler = {"up": (answer.votes_up, answer.votes_down), "down": (answer.votes_down, answer.votes_up)}
        self.toggle_votes(pk_question, *handler[votes_do])
        return redirect(reverse('detail_question', args=pk_question))


class ToggleAnswerRightClass(LoginRequiredMixin, View):
    login_url = '/account/login/'
    http_method_names = ['get', ]

    def dispatch(self, request, *args, **kwargs):
        if "pk_question" not in kwargs.keys():
            return self.handle_no_permission()
        if self.request.user != Question.objects.get(pk=kwargs['pk_question']).author:
            return self.handle_no_permission()
        return super(ToggleAnswerRightClass, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk_question, pk, **kwargs):
        answer = Answer.objects.get(pk=pk)
        answer.right = not answer.right
        answer.save()
        return redirect(reverse('detail_question', args=self.kwargs['pk_question']))
