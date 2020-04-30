from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from hasker import settings
from question_and_answer.views import HomePageTemplate, QuestionCreateView, DetailQuestion, ChangeVotesClass, \
    ChangeVotesAnswerClass, ToggleAnswerRightClass, SearchQuestion

urlpatterns = [
                  path('account/', include('account.urls')),
                  path('admin/', admin.site.urls),
                  path('', include('question_and_answer.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path


def trigger_error(request):
    division_by_zero = 1 / 0


if settings.URL_PREFIX_TO_CHECK_SENTRY:
    urlpatterns += [
        path(f'sentry-debug-{settings.URL_PREFIX_TO_CHECK_SENTRY}/', trigger_error),
    ]
