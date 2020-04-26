from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.db.models import Count, F
from django.urls import reverse

MIDDLE_LENGTH = 200
SMALL_LENGTH = 50

User = get_user_model()


class SortedByVotesQuerySet(models.QuerySet):
    def order_by_votes_and_date(self):
        return self.annotate(up=Count('votes_up')).annotate(down=Count('votes_down')).\
            order_by(F('down') - F('up'), '-date')


class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    votes_up = models.ManyToManyField(User, related_name='user_votes_up')
    votes_down = models.ManyToManyField(User, related_name='user_votes_down')
    objects = SortedByVotesQuerySet.as_manager()

    @property
    def votes(self):
        return self.votes_up.count() - self.votes_down.count()

    class Meta:
        abstract = True


class Tags(models.Model):
    label = models.CharField(max_length=SMALL_LENGTH, unique=True)


class Question(Message):
    max_tags = 3
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tags)

    @property
    def answer_count(self):
        return self.answer_set.count()

    def get_absolute_url(self):
        return reverse('detail_question', args=[str(self.pk)])


class Answer(Message):
    paginate = 30
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    right = models.BooleanField(default=False)
    votes_up = models.ManyToManyField(User, related_name='user_votes_answer_up')
    votes_down = models.ManyToManyField(User, related_name='user_votes_answer_down')

    def get_absolute_url_to_toggle_answer_as_right(self):
        return f"{reverse('detail_question', args=[str(self.question.pk)])}answer/{self.pk}/right/"

    def get_absolute_url(self):
        return f"{reverse('detail_question', args=[str(self.question.pk)])}answer/{self.pk}/"

    def get_all_votes_user(self):
        return self.votes_up.all().union(self.votes_down.all())

    def toggle_right(self):
        self.right = not self.right
