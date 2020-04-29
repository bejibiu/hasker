from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from hasker import settings
from question_and_answer.views import HomePageTemplate, QuestionCreateView, DetailQuestion, ChangeVotesClass, \
    ChangeVotesAnswerClass, ToggleAnswerRightClass, SearchQuestion

urlpatterns = [
                  path('', HomePageTemplate.as_view(), name='home'),
                  path('account/', include('account.urls')),
                  path('admin/', admin.site.urls),
                  path('save-question/', QuestionCreateView.as_view(), name='save_question'),
                  re_path(r'^question/(?P<pk>\d+)/(?P<votes_do>up|down)/$', ChangeVotesClass.as_view(),
                          name='votes_question'),
                  re_path(r'^question/(?P<pk_question>\d+)/answer/(?P<pk>\d+)/(?P<votes_do>up|down)/$',
                          ChangeVotesAnswerClass.as_view(), name='votes_answer'),
                  re_path(r'^question/(?P<pk_question>\d+)/answer/(?P<pk>\d+)/right/$',
                          ToggleAnswerRightClass.as_view(), name='right_class'),
                  path('question/<int:pk>/', DetailQuestion.as_view(), name='detail_question'),
                  path('search', SearchQuestion.as_view(), name='search_question')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path


def trigger_error(request):
    division_by_zero = 1 / 0


if settings.URL_PREFIX_TO_CHECK_SENTRY:
    urlpatterns += [
        path(f'sentry-debug-{settings.URL_PREFIX_TO_CHECK_SENTRY}/', trigger_error),
    ]
