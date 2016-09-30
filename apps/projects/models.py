from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.models import Model
from apps.domain.models import Attribute, Option
from apps.questions.models import Catalog


@python_2_unicode_compatible
class Project(Model):

    owner = models.ManyToManyField(User)

    title = models.CharField(max_length=256, verbose_name=_('title'))
    description = models.TextField(blank=True, help_text=_('Optional'), verbose_name=_('description'))

    catalog = models.ForeignKey(Catalog, related_name='+', help_text=_('The catalog which will be used for this project.'), verbose_name=_('catalog'))

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

    @property
    def current_values(self):
        return self.values.filter(snapshot=None)


@python_2_unicode_compatible
class Snapshot(Model):

    title = models.CharField(max_length=256, verbose_name=_('title'))
    description = models.TextField(blank=True, help_text=_('Optional'), verbose_name=_('description'))

    project = models.ForeignKey('Project', related_name='snapshots')

    class Meta:
        ordering = ('project', '-created')
        verbose_name = _('Snapshot')
        verbose_name_plural = _('Snapshots')

    def __str__(self):
        return '%s / %s' % (self.project.title, self.title)

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.project.pk})

    def rollback(self):
        # first remove all current values
        Value.objects.filter(snapshot=None).delete()

        # remove the snapshot from current_snapshot.values
        for value in self.values.all():
            value.snapshot = None
            value.save()

        # remove all snapshot created later and the current_snapshot
        for snapshot in Snapshot.objects.filter(created__gte=self.created):
            snapshot.delete()


def create_values_for_snapshot(sender, **kwargs):
    snapshot = kwargs['instance']
    if kwargs['created'] and not kwargs.get('raw', False):
        # gather values without snapshot
        current_values = Value.objects.filter(project=snapshot.project, snapshot=None)

        # loop over values and save a copy with a fk to the snapshot
        for value in current_values:
            value.pk = None
            value.snapshot = snapshot
            value.save()

post_save.connect(create_values_for_snapshot, sender=Snapshot)


@python_2_unicode_compatible
class Value(Model):

    project = models.ForeignKey('Project', related_name='values')
    snapshot = models.ForeignKey('Snapshot', blank=True, null=True, related_name='values')

    attribute = models.ForeignKey(Attribute, related_name='values', blank=True, null=True, on_delete=models.SET_NULL)

    set_index = models.IntegerField(default=0)
    collection_index = models.IntegerField(default=0)

    text = models.TextField(blank=True, null=True)
    option = models.ForeignKey(Option, blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        verbose_name = _('Value')
        verbose_name_plural = _('Values')

    def __str__(self):
        if self.attribute:
            attribute_label = self.attribute.label
        else:
            attribute_label = 'none'

        if self.snapshot:
            snapshot_title = self.snapshot.title
        else:
            snapshot_title = _('current')

        return '%s / %s / %s.%i.%i = "%s"' % (
            self.project.title,
            snapshot_title,
            attribute_label,
            self.set_index,
            self.collection_index,
            self.value
        )

    @property
    def value(self):
        if self.option:
            if self.option.additional_input:
                return self.option.text + ': ' + self.text
            else:
                return self.option.text
        elif self.text:
            return self.text
        else:
            return None
