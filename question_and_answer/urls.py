from django.urls import path, re_path

from .views import (
    HomePageTemplate,
    QuestionCreateView,
    ChangeVotesClass,
    ChangeVotesAnswerClass,
    DetailQuestion,
    SearchQuestion,
    ToggleAnswerCorrectClass,
)

urlpatterns = [
    path("", HomePageTemplate.as_view(), name="home"),
    path("save-question/", QuestionCreateView.as_view(), name="save_question"),
    re_path(
        r"^question/(?P<pk>\d+)/(?P<votes_do>up|down)/$",
        ChangeVotesClass.as_view(),
        name="votes_question",
    ),
    re_path(
        r"^question/(?P<pk_question>\d+)/answer/(?P<pk>\d+)/(?P<votes_do>up|down)/$",
        ChangeVotesAnswerClass.as_view(),
        name="votes_answer",
    ),
    re_path(
        r"^question/(?P<pk_question>\d+)/answer/(?P<pk>\d+)/correct/$",
        ToggleAnswerCorrectClass.as_view(),
        name="correct_class",
    ),
    path("question/<int:pk>/", DetailQuestion.as_view(), name="detail_question"),
    path("search", SearchQuestion.as_view(), name="search_question"),
]
