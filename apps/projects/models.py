from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.models import Model
from apps.domain.models import Attribute, AttributeSet
from apps.questions.models import Catalog


@python_2_unicode_compatible
class Project(Model):

    owner = models.ManyToManyField(User)

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, help_text=_('You can use markdown syntax in the description.'))

    current_snapshot = models.ForeignKey('Snapshot', null=True, blank=True, related_name='+')
    catalog = models.ForeignKey(Catalog, related_name='+', help_text=_('The catalog which will be used for this project.'))

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
        project.current_snapshot = Snapshot.objects.create(project=project)
        project.save()


post_save.connect(create_snapshot_for_project, sender=Project)


@python_2_unicode_compatible
class Snapshot(Model):

    project = models.ForeignKey('Project', related_name='snapshots')

    class Meta:
        ordering = ('project', 'pk')
        verbose_name = _('Snapshot')
        verbose_name_plural = _('Snapshots')

    def __str__(self):
        return '%s[%i]' % (self.project.title, self.pk)


class ValueEntity(Model):

    snapshot = models.ForeignKey('Snapshot', related_name='entities')
    index = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('ValueEntity')
        verbose_name_plural = _('ValueEntities')


@python_2_unicode_compatible
class ValueSet(ValueEntity):

    attributeset = models.ForeignKey(AttributeSet, blank=True, null=True, on_delete=models.SET_NULL, related_name='valuesets')

    class Meta:
        verbose_name = _('ValueSet')
        verbose_name_plural = _('ValueSet')

    def __str__(self):
        return '%s[%s] / %s[%i]' % (self.snapshot.project.title, self.snapshot.pk, self.tag, self.index)

    @property
    def tag(self):
        if self.attributeset:
            return self.attributeset.tag
        else:
            return 'none'


@python_2_unicode_compatible
class Value(ValueEntity):

    valueset = models.ForeignKey('ValueSet', blank=True, null=True, on_delete=models.SET_NULL, related_name='values')

    attribute = models.ForeignKey(Attribute, related_name='values')
    text = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Value')
        verbose_name_plural = _('Values')

    def __str__(self):
        if self.valueset:
            return '%s / %s[%i].%s[%i]' % (self.snapshot, self.valueset.attributeset.tag, self.valueset.index, self.tag, self.index)
        else:
            return '%s / %s' % (self.snapshot, self.attribute.tag)

    @property
    def tag(self):
        if self.attribute:
            return self.attribute.tag
        else:
            return 'none'
