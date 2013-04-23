from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager
from tastypie.models import create_api_key
from django.db.models.signals import post_save

class Task(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=500)
    tags = TaggableManager()
    due_date = models.DateField()

    def __unicode__(self):
        return self.title

models.signals.post_save.connect(create_api_key, sender=User)
