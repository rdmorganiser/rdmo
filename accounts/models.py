from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

from jsonfield import JSONField


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User)
    details = JSONField(null=True, blank=True)

    class Meta:
        ordering = ("user",)

    def __str__(self):
        return self.user.username


@python_2_unicode_compatible
class DetailKey(models.Model):

    TYPE_CHOICES = (
        ('text', 'Input field'),
        ('textarea', 'Textarea field'),
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio button'),
        ('select', 'Select field'),
        ('multiselect', 'Multiselect field'),
    )

    key = models.SlugField()
    label = models.CharField(max_length=256)
    type = models.CharField(max_length=11, choices=TYPE_CHOICES)
    help_text = models.TextField(blank=True)
    options = JSONField(null=True, blank=True, help_text="Enter valid JSON of the form [[key, label], [key, label], ...]")
    required = models.BooleanField()

    def __str__(self):
        return self.key


def create_profile_for_user(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        profile = Profile()
        profile.user = user
        profile.save()

post_save.connect(create_profile_for_user, sender=User)
