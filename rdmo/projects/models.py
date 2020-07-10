import iso8601
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from rdmo.core.constants import (VALUE_TYPE_BOOLEAN, VALUE_TYPE_CHOICES,
                                 VALUE_TYPE_DATETIME, VALUE_TYPE_TEXT)
from rdmo.core.models import Model
from rdmo.domain.models import Attribute
from rdmo.options.models import Option
from rdmo.questions.models import Catalog, Question
from rdmo.tasks.models import Task
from rdmo.views.models import View

from .managers import (MembershipManager, ProjectManager, SnapshotManager,
                       ValueManager)


class Project(Model):

    objects = ProjectManager()

    user = models.ManyToManyField(
        User, through='Membership',
        verbose_name=_('User'),
        help_text=_('The list of users for this project.')
    )
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE,
        verbose_name=_('Site'),
        help_text=_('The site this project belongs to (in a multi site setup).')
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
        Catalog, related_name='+', on_delete=models.SET_NULL, null=True,
        verbose_name=_('Catalog'),
        help_text=_('The catalog which will be used for this project.')
    )
    tasks = models.ManyToManyField(
        Task, blank=True,
        verbose_name=_('Tasks'),
        help_text=_('The tasks that will be used for this project.')
    )
    views = models.ManyToManyField(
        View, blank=True,
        verbose_name=_('Views'),
        help_text=_('The views that will be used for this project.')
    )

    class Meta:
        ordering = ('title', )
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.pk})

    @cached_property
    def member(self):
        return self.user.all()

    @cached_property
    def owners_str(self):
        return ', '.join(['' if x is None else str(x) for x in self.user.filter(membership__role='owner')])

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


class Membership(models.Model):

    objects = MembershipManager()

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

    def __str__(self):
        return '%s / %s / %s' % (self.project.title, self.user.username, self.role)

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.project.pk})


class Snapshot(Model):

    objects = SnapshotManager()

    project = models.ForeignKey(
        'Project', related_name='snapshots',
        on_delete=models.CASCADE, null=True,
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

    def save(self, *args, **kwargs):
        copy_values = kwargs.pop('copy_values', True)
        super().save()

        if copy_values:
            # loop over values without snapshot and save a copy with a fk to the snapshot
            for value in self.project.values.filter(snapshot=None):
                value.pk = None
                value.snapshot = self
                value.save()

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


class Value(Model):

    objects = ValueManager()

    FALSE_TEXT = [None, '', '0', 'f', 'F', 'false', 'False']

    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, related_name='values',
        verbose_name=_('Project'),
        help_text=_('The project this value belongs to.')
    )
    snapshot = models.ForeignKey(
        'Snapshot', blank=True, null=True,
        on_delete=models.CASCADE, related_name='values',
        verbose_name=_('Snapshot'),
        help_text=_('The snapshot this value belongs to.')
    )
    attribute = models.ForeignKey(
        Attribute, blank=True, null=True,
        on_delete=models.SET_NULL, related_name='values',
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
        blank=True,
        verbose_name=_('Text'),
        help_text=_('The string stored for this value.')
    )
    option = models.ForeignKey(
        Option, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Option'),
        help_text=_('The option stored for this value.')
    )
    value_type = models.CharField(
        max_length=8, choices=VALUE_TYPE_CHOICES, default=VALUE_TYPE_TEXT,
        verbose_name=_('Value type'),
        help_text=_('Type of this value.')
    )
    unit = models.CharField(
        max_length=64, blank=True,
        verbose_name=_('Unit'),
        help_text=_('Unit for this value.')
    )

    class Meta:
        ordering = ('attribute', 'set_index', 'collection_index' )
        verbose_name = _('Value')
        verbose_name_plural = _('Values')

    # def __str__(self):
    #     if self.attribute:
    #         attribute_label = self.attribute.path
    #     else:
    #         attribute_label = 'none'

    #     if self.snapshot:
    #         snapshot_title = self.snapshot.title
    #     else:
    #         snapshot_title = _('current')

    #     return '%s / %s / %s.%i.%i = "%s"' % (
    #         self.project.title,
    #         snapshot_title,
    #         attribute_label,
    #         self.set_index,
    #         self.collection_index,
    #         self.value
    #     )

    @property
    def value(self):
        if self.option:
            value = self.option.text or ''
            if self.option.additional_input and self.text:
                value += ': ' + self.text
            return value

        elif self.text:
            if self.value_type == VALUE_TYPE_DATETIME:
                try:
                    return iso8601.parse_date(self.text).date()
                except iso8601.ParseError:
                    return self.text
            elif self.value_type == VALUE_TYPE_BOOLEAN:
                if self.text == '1':
                    return _('Yes')
                else:
                    return _('No')
            else:
                return self.text
        else:
            return None

    @property
    def value_and_unit(self):
        value = self.value

        if value is None:
            return ''
        elif self.unit:
            return '%s %s' % (value, self.unit)
        else:
            return value

    @property
    def is_true(self):
        return self.text not in self.FALSE_TEXT

    @property
    def is_false(self):
        return self.text in self.FALSE_TEXT

    @property
    def as_number(self):
        try:
            val = self.text
        except AttributeError:
            return 0
        else:
            if isinstance(val, str):
                val = val.replace(',', '.')
            if isinstance(val, float) is False:
                try:
                    return int(val)
                except ValueError:
                    pass
                try:
                    return float(val)
                except ValueError:
                    return 0
            else:
                return val

    def get_question(self, catalog):
        if self.attribute is not None:
            return Question.objects.filter(questionset__section__catalog=catalog).filter(
                attribute=self.attribute
            ).first()
        else:
            return None

    def get_current_value(self, current_project):
        if (self.attribute is not None) and (current_project is not None):
            return current_project.values.filter(
                snapshot=None,
                attribute=self.attribute,
                set_index=self.set_index,
                collection_index=self.collection_index
            ).first()
        else:
            return None
