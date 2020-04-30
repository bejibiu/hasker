from django.contrib import admin

from question_and_answer.models import Question, Tags, Answer


class AnswerInstanceInline(admin.TabularInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInstanceInline]


admin.site.register(Tags)
