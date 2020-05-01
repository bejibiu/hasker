from django.views.generic.list import MultipleObjectMixin

from .models import Question


class PopularQuestionMixin(MultipleObjectMixin):
    max_popular_questions = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        popular_questions = Question.objects.all().order_by_votes_and_date()[
                            : self.max_popular_questions
                            ]
        context = {"popular_questions": popular_questions}
        context.update(kwargs)
        return super().get_context_data(**context)
