from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Project(models.Model):

    owner = models.ManyToManyField(User)

    name = models.CharField(max_length=256)
    pi = models.CharField(max_length=256)
    description = models.TextField(blank=True)

    def owner_string(self):
        return ', '.join([user.profile.full_name for user in self.owner.all()])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('name', )
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


def add_owner_to_project(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        project = Project()
        project.owner.add(user)
        project.save()


post_save.connect(add_owner_to_project, sender=User)
