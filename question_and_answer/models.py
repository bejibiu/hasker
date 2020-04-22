from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.urls import reverse

MIDDLE_LENGTH = 200
SMALL_LENGTH = 50

User = get_user_model()


class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    user_votes = models.ManyToManyField(User, related_name='user_votes')
    votes = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Tags(models.Model):
    label = models.CharField(max_length=SMALL_LENGTH)


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
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    user_votes = models.ManyToManyField(User, related_name='user_answer_votes')
