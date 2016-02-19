from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.models import Model


@python_2_unicode_compatible
class Project(Model):

    owner = models.ManyToManyField(User)

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, help_text=_('You can use markdown syntax in the description.'))

    current_snapshot = models.ForeignKey('Snapshot', null=True, blank=True, related_name='+')

    class Meta:
        ordering = ('title', )
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.pk})

    def owner_string(self):
        return ', '.join([user.profile.full_name for user in self.owner.all()])


def create_snapshot_for_project(sender, **kwargs):
    project = kwargs['instance']
    if kwargs['created']:
        project.current_snapshot == Snapshot.objects.create(project=project)
        project.save()


post_save.connect(create_snapshot_for_project, sender=Project)


@python_2_unicode_compatible
class Snapshot(Model):

    project = models.ForeignKey('Project', related_name='snapshots')

    class Meta:
        ordering = ('project', 'pk')
        verbose_name = _('Snapshot')
        verbose_name_plural = _('Snapshots')


@python_2_unicode_compatible
class Entity(Model):

    snapshot = models.ForeignKey('Snapshot', related_name='entities')

    class Meta:
        verbose_name = _('Entity')
        verbose_name_plural = _('Entities')


@python_2_unicode_compatible
class Collection(Entity):

    class Meta:
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')


@python_2_unicode_compatible
class Value(Entity):

    belongs_to = models.ForeignKey('Collection', blank=True, null=True, related_name='values')
    text = models.TextField()

    class Meta:
        verbose_name = _('Value')
        verbose_name_plural = _('Values')
