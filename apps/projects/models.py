from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Project(models.Model):

    owner = models.ManyToManyField(User)

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, help_text=_('You can use markdown syntax in the description.'))

    def owner_string(self):
        return ', '.join([user.profile.full_name for user in self.owner.all()])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('title', )
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
