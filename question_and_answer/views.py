from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import mail
from django.db.models import F, Count, Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin

from question_and_answer.forms import QuestionForm, AnswerForm
from question_and_answer.models import Question, Tags, Answer


class PopularQuestionMixin(MultipleObjectMixin):
    max_popular_questions = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        popular_questions = Question.objects.all().order_by_votes_and_date()[
            : self.max_popular_questions
        ]
        context = {"popular_questions": popular_questions}
        context.update(kwargs)
        return super().get_context_data(**context)


class HomePageTemplate(ListView, PopularQuestionMixin):
    model = Question
    template_name = "index.html"
    paginate_by = 20

    def get_queryset(self):
        queryset = super(HomePageTemplate, self).get_queryset()
        ordering = self.request.GET.get("sorted") or "-date"
        queryset = (
            queryset.order_by_votes_and_date()
            if ordering == "vote"
            else queryset.order_by("-date")
        )
        return queryset


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm

    def post(self, request, *args, **kwargs):
        question_form = self.form_class(request.POST)

        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.author = request.user
            question.save()
            for tag in question_form.cleaned_data["tags"]:
                question.tags.add((Tags.objects.get_or_create(label=tag))[0])
            messages.success(self.request, "Ask saved successfully")
            return redirect(question.get_absolute_url())
        return render(request, "index.html", {"question_form": question_form})


class SearchQuestion(ListView, PopularQuestionMixin):
    model = Question
    template_name = "search.html"
    paginate_by = 20
    tag_search_prefix = "tag:"

    def get_queryset(self):
        queryset = super(SearchQuestion, self).get_queryset()
        query = self.request.GET.get("q")
        if query.startswith(self.tag_search_prefix):
            query = query[len(self.tag_search_prefix) :]
            queryset = queryset.filter(tags__label=query)
        else:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(text__icontains=query)
            )
        queryset = queryset.order_by_votes_and_date()
        return queryset


class DetailQuestion(DetailView, FormMixin, PopularQuestionMixin):
    model = Question
    form_class = AnswerForm
    http_method_names = ["get", "post"]
    paginate_by = 30

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object_list = (
            self.object.answer_set.all()
            .annotate(up=Count("votes_up"))
            .annotate(down=Count("votes_down"))
            .order_by("-correct", F("down") - F("up"), "date")
        )
        context = self.get_context_data(
            object=self.object, object_list=self.object_list
        )
        return self.render_to_response(context)

    def post(self, request, pk):
        self.object = self.get_object()
        form_answer = self.form_class(request.POST)
        if form_answer.is_valid():
            answer = form_answer.save(commit=False)
            answer.author = request.user
            answer.question = self.object
            answer.save()
            url = request.build_absolute_uri(self.object.get_absolute_url())
            mail.send_mail(
                "YOU GOT AN ANSWER",
                f"Hi friend. For your question, added the answer\n Use this link to you'r answer"
                f" {url}",
                settings.EMAIL_HOST_USER,
                [self.object.author.email],
            )
            messages.success(self.request, "Answer saved successfully")
            return redirect(self.object.get_absolute_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ChangeVotesClass(LoginRequiredMixin, View):
    login_url = "/account/login/"
    http_method_names = [
        "get",
    ]

    def toggle_votes(self, selected_list_voted, another_list_voted):
        if self.request.user in selected_list_voted.all():
            selected_list_voted.remove(self.request.user)
            return
        selected_list_voted.add(self.request.user)
        if self.request.user in another_list_voted.all():
            another_list_voted.remove(self.request.user)

    def get(self, request, pk, votes_do):
        question = Question.objects.get(pk=pk)
        handler = {
            "up": (question.votes_up, question.votes_down),
            "down": (question.votes_down, question.votes_up),
        }
        self.toggle_votes(*handler[votes_do])
        return redirect(question.get_absolute_url())


class ChangeVotesAnswerClass(LoginRequiredMixin, View):
    login_url = "/account/login/"
    http_method_names = [
        "get",
    ]

    def toggle_votes(self, pk_question, selected_list_voted, another_list_voted):
        if self.request.user in selected_list_voted.all():
            selected_list_voted.remove(self.request.user)
            return
        [
            answer.votes_down.remove(self.request.user)
            for answer in Answer.objects.filter(question_id=pk_question).filter(
                votes_down=self.request.user
            )
        ]
        [
            answer.votes_up.remove(self.request.user)
            for answer in Answer.objects.filter(question_id=pk_question).filter(
                votes_up=self.request.user
            )
        ]
        selected_list_voted.add(self.request.user)
        if self.request.user in another_list_voted.all():
            another_list_voted.remove(self.request.user)

    def get(self, request, pk_question, pk, votes_do):
        answer = Answer.objects.get(pk=pk)
        handler = {
            "up": (answer.votes_up, answer.votes_down),
            "down": (answer.votes_down, answer.votes_up),
        }
        self.toggle_votes(pk_question, *handler[votes_do])
        return redirect(answer.question.get_absolute_url())


class ToggleAnswerCorrectClass(LoginRequiredMixin, View):
    login_url = "/account/login/"
    http_method_names = [
        "get",
    ]

    def dispatch(self, request, *args, **kwargs):
        if "pk_question" not in kwargs.keys():
            return self.handle_no_permission()
        if self.request.user != Question.objects.get(pk=kwargs["pk_question"]).author:
            return self.handle_no_permission()
        return super(ToggleAnswerCorrectClass, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk_question, pk, **kwargs):
        answer = Answer.objects.get(pk=pk)
        if answer.correct is False:
            for correct_answer in Answer.objects.filter(question_id=pk_question).filter(
                correct=True
            ):
                correct_answer.toggle_correct()
                correct_answer.save()
        answer.toggle_correct()
        answer.save()
        return redirect(answer.question.get_absolute_url())
