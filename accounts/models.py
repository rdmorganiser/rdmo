from __future__ import unicode_literals

from django.db import models
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
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    hint = models.TextField(blank=True)
    options = JSONField(null=True, blank=True)
    required = models.BooleanField()

    def __str__(self):
        return self.key
