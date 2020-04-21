from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.urls import reverse

MIDDLE_LENGTH = 200
SMALL_LENGTH = 50

User = get_user_model()


class Tags(models.Model):
    label = models.CharField(max_length=SMALL_LENGTH)


class Question(models.Model):
    max_tags = 3
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)
    user_votes = models.ManyToManyField(User, related_name='user_votes')

    @property
    def votes(self):
        return self.user_votes.count()

    @property
    def answer_count(self):
        return self.answer_set.count()

    def get_absolute_url(self):
        return reverse('detail_question', args=[str(self.pk)])


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(default=False)
