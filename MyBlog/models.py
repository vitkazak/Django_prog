from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = RichTextField()
    preview = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_user(self):
        return self.user


class Friend(models.Model):
    class Meta:
        db_table = 'Friend'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name="friends", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Subscriber(models.Model):
    email = models.EmailField('', max_length=100, null=True, blank=True)
