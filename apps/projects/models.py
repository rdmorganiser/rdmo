from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.models import Model
from apps.domain.models import Attribute
from apps.options.models import Option
from apps.questions.models import Catalog


@python_2_unicode_compatible
class Project(Model):

    owner = models.ManyToManyField(
        User,
        verbose_name=_('Owner'),
        help_text=_('The list of owners for this project.')
    )
    title = models.CharField(
        max_length=256,
        verbose_name=_('Title'),
        help_text=_('The title for this project.')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_('A description for this project (optional).')
    )
    catalog = models.ForeignKey(
        Catalog, related_name='+',
        verbose_name=_('Catalog'),
        help_text=_('The catalog which will be used for this project.')
    )

    class Meta:
        ordering = ('title', )
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.pk})

    def owner_string(self):
        return ', '.join([user.username for user in self.owner.all()])

    @property
    def current_values(self):
        return self.values.filter(snapshot=None)


@python_2_unicode_compatible
class Snapshot(Model):

    project = models.ForeignKey(
        'Project', related_name='snapshots',
        verbose_name=_('Project'),
        help_text=_('The project this snapshot belongs to.')
    )
    title = models.CharField(
        max_length=256,
        verbose_name=_('Title'),
        help_text=_('The title for this snapshot.')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_('A description for this snapshot (optional).')
    )

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

        # remove the snapshot from this snapshots values
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

    project = models.ForeignKey(
        'Project', related_name='values',
        verbose_name=_('Project'),
        help_text=_('The project this value belongs to.')
    )
    snapshot = models.ForeignKey(
        'Snapshot', blank=True, null=True, related_name='values',
        verbose_name=_('Snapshot'),
        help_text=_('The snapshot this value belongs to.')
    )
    attribute = models.ForeignKey(
        Attribute, related_name='values', blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name=_('Attribute'),
        help_text=_('The attribute this value belongs to.')
    )
    set_index = models.IntegerField(
        default=0,
        verbose_name=_('Set index'),
        help_text=_('The position of this value in an entity collection (i.e. in the question set)')
    )
    collection_index = models.IntegerField(
        default=0,
        verbose_name=_('Collection index'),
        help_text=_('The position of this value in an attribute collection.')
    )
    text = models.TextField(
        blank=True, null=True,
        verbose_name=_('Text'),
        help_text=_('The string stored for this value.')
    )
    option = models.ForeignKey(
        Option, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Option'),
        help_text=_('The option stored for this value.')
    )

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
