from __future__ import unicode_literals

import iso8601

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.models import TranslationMixin
from apps.domain.models import Attribute
from apps.conditions.models import Condition


@python_2_unicode_compatible
class Task(TranslationMixin, models.Model):

    attribute = models.ForeignKey(Attribute, blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    time_period = models.DurationField()

    title_en = models.CharField(max_length=256)
    title_de = models.CharField(max_length=256)

    text_en = models.CharField(max_length=256)
    text_de = models.CharField(max_length=256)

    conditions = models.ManyToManyField(Condition, blank=True)

    class Meta:
        ordering = ('attribute',)
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.title

    @property
    def title(self):
        return self.trans('title')

    @property
    def text(self):
        return self.trans('text')

    def get_deadline(self, snapshot):
        values = snapshot.values.filter(attribute=self.attribute)

        for value in values:
            try:
                return iso8601.parse_date(value.text) + self.time_period
            except iso8601.ParseError:
                return None
