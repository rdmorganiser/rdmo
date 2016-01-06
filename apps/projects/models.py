from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Project(models.Model):

    owner = models.ManyToManyField(User)

    name = models.CharField(max_length=256)
    pi = models.CharField(max_length=256)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
