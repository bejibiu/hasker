from django.db import models
from django.conf import settings

MIIDLE_LENGTH = 200
SMALL_LENGTH = 50


class Tags(models.Model):
    lable = models.CharField(max_length=SMALL_LENGTH)


class Question(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)


class Asnwer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(default=False)
