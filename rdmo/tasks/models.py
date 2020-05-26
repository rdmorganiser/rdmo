from datetime import date, timedelta
from itertools import zip_longest

from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _

from rdmo.conditions.models import Condition
from rdmo.core.models import TranslationMixin
from rdmo.core.utils import get_uri_prefix
from rdmo.domain.models import Attribute

from .managers import TaskManager
from .validators import TaskUniqueKeyValidator


class Task(TranslationMixin, models.Model):

    objects = TaskManager()

    uri = models.URLField(
        max_length=640, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this task (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this task.')
    )
    key = models.SlugField(
        max_length=128, blank=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this task.')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this task.')
    )
    sites = models.ManyToManyField(
        Site, blank=True,
        verbose_name=_('Sites'),
        help_text=_('The sites this task belongs to (in a multi site setup).')
    )
    groups = models.ManyToManyField(
        Group, blank=True,
        verbose_name=_('Group'),
        help_text=_('The groups for which this task is active.')
    )
    title_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (primary)'),
        help_text=_('The title for this task in the primary language.')
    )
    title_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (secondary)'),
        help_text=_('The title for this task in the secondary language.')
    )
    title_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (tertiary)'),
        help_text=_('The title for this task in the tertiary language.')
    )
    title_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quaternary)'),
        help_text=_('The title for this task in the quaternary language.')
    )
    title_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quinary)'),
        help_text=_('The title for this task in the quinary language.')
    )
    text_lang1 = models.TextField(
        blank=True,
        verbose_name=_('Text (primary)'),
        help_text=_('The text for this task in the primary language.')
    )
    text_lang2 = models.TextField(
        blank=True,
        verbose_name=_('Text (secondary)'),
        help_text=_('The text for this task in the secondary language.')
    )
    text_lang3 = models.TextField(
        blank=True,
        verbose_name=_('Text (tertiary)'),
        help_text=_('The text for this task in the tertiary language.')
    )
    text_lang4 = models.TextField(
        blank=True,
        verbose_name=_('Text (quaternary)'),
        help_text=_('The text for this task in the quaternary language.')
    )
    text_lang5 = models.TextField(
        blank=True,
        verbose_name=_('Text (quinary)'),
        help_text=_('The text for this task in the quinary language.')
    )
    start_attribute = models.ForeignKey(
        Attribute, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Start date attribute'),
        help_text=_('The attribute that is setting the start date for this task.')
    )
    end_attribute = models.ForeignKey(
        Attribute, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('End date attribute'),
        help_text=_('The attribute that is setting the end date for this task (optional, if no end date attribute is given, the start date attribute sets also the end date).')
    )
    days_before = models.IntegerField(
        blank=True, null=True,
        verbose_name=_('Days before'),
        help_text=_('Additional days before the start date.')
    )
    days_after = models.IntegerField(
        blank=True, null=True,
        verbose_name=_('Days after'),
        help_text=_('Additional days after the end date.')
    )
    conditions = models.ManyToManyField(
        Condition, blank=True,
        verbose_name=_('Conditions'),
        help_text=_('The list of conditions evaluated for this task.')
    )

    class Meta:
        ordering = ('uri',)
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        self.uri = self.build_uri()
        super(Task, self).save(*args, **kwargs)

    def clean(self):
        TaskUniqueKeyValidator(self).validate()

    @property
    def title(self):
        return self.trans('title')

    @property
    def text(self):
        return self.trans('text')

    @property
    def has_conditions(self):
        return bool(self.conditions.all())

    def build_uri(self):
        return get_uri_prefix(self) + '/tasks/' + self.key

    def get_dates(self, values):
        if self.start_attribute:
            start_values = values.filter(attribute=self.start_attribute)
        else:
            start_values = []

        if self.end_attribute:
            end_values = values.filter(attribute=self.end_attribute)
        else:
            end_values = []

        days_before = timedelta(self.days_before) if self.days_before else timedelta()
        days_after = timedelta(self.days_after) if self.days_after else timedelta()

        dates = []
        for start_value, end_value in zip_longest(start_values, end_values):

            if start_value and start_value.value and isinstance(start_value.value, date):
                start_date = start_value.value
            else:
                start_date = None

            if end_value and end_value.value and isinstance(end_value.value, date):
                end_date = end_value.value
            else:
                end_date = None

            if start_date and end_date:
                dates.append((start_date - days_before, end_date + days_after))
            elif start_date:
                dates.append((start_date - days_before + days_after, ))
            elif end_date:
                dates.append((end_date - days_before + days_after, ))

        return dates
