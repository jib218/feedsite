from django.db import models
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField

# Create your models here.


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=42)

    def __str__(self):
        return self.title

class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()
    categories = models.ManyToManyField(Category)
    bozo = models.BooleanField(default=False)
    lastchecked = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class Item(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    link = models.URLField()
    published = models.DateTimeField()
    tags = models.TextField(null=True, blank=True)
    isRead = models.BooleanField(default=False)
    unique_feed_id = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Settings(models.Model):
    import pytz
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    user = AutoOneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    delete_older_than_days = models.PositiveSmallIntegerField(default=7)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')