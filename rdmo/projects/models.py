from __future__ import unicode_literals

import iso8601

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from rdmo.core.models import Model
from rdmo.domain.models import Attribute
from rdmo.options.models import Option
from rdmo.questions.models import Catalog


@python_2_unicode_compatible
class Project(Model):

    user = models.ManyToManyField(
        User, through='Membership',
        verbose_name=_('User'),
        help_text=_('The list of users for this project.')
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
        permissions = (('view_project', 'Can view project'),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.pk})

    @cached_property
    def member(self):
        return self.user.all()

    @cached_property
    def owners(self):
        return self.user.filter(membership__role='owner')

    @cached_property
    def managers(self):
        return self.user.filter(membership__role='manager')

    @cached_property
    def authors(self):
        return self.user.filter(membership__role='author')

    @cached_property
    def guests(self):
        return self.user.filter(membership__role='guest')


@python_2_unicode_compatible
class Membership(models.Model):

    ROLE_CHOICES = (
        ('owner', _('Owner')),
        ('manager', _('Manager')),
        ('author', _('Author')),
        ('guest', _('Guest')),
    )

    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE,
        verbose_name=_('Project'),
        help_text=_('The project for this membership.')
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name=_('User'),
        help_text=_('The user for this membership.')
    )
    role = models.CharField(
        max_length=12, choices=ROLE_CHOICES,
        verbose_name=_('Role'),
        help_text=_('The role for this membership.')
    )

    class Meta:
        ordering = ('project__title', )
        verbose_name = _('Membership')
        verbose_name_plural = _('Memberships')
        permissions = (('view_membership', 'Can view membership'),)

    def __str__(self):
        return '%s / %s / %s' % (self.project.title, self.user.username, self.role)

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.project.pk})


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
        permissions = (('view_snapshot', 'Can view snapshot'),)

    def __str__(self):
        return '%s / %s' % (self.project.title, self.title)

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.project.pk})

    def rollback(self):
        # remove all current values for this project
        self.project.values.filter(snapshot=None).delete()

        # remove the snapshot_id from this snapshots values so they are current values
        for value in self.values.all():
            value.snapshot = None
            value.save()

        # remove all snapshot created later and the current_snapshot
        # this also removes the values of these snapshots
        for snapshot in self.project.snapshots.filter(created__gte=self.created):
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
        permissions = (('view_value', 'Can view value'),)

    def __str__(self):
        if self.attribute:
            attribute_label = self.attribute.path
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

            if self.attribute.value_type == Attribute.VALUE_TYPE_DATETIME:
                try:
                    return iso8601.parse_date(self.text).date()
                except iso8601.ParseError:
                    return self.text
            elif self.attribute.value_type == Attribute.VALUE_TYPE_BOOLEAN:
                if self.text == '1':
                    return _('yes')
                else:
                    return _('no')
            else:
                return self.text
        else:
            return None

    @property
    def value_and_unit(self):
        value = self.value

        if value == None:
            return ''
        elif self.attribute.unit:
            return '%s %s' % (value, self.attribute.unit)
        else:
            return value
