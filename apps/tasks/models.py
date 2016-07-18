from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.models import TranslationMixin
from apps.domain.models import Attribute


@python_2_unicode_compatible
class Task(TranslationMixin, models.Model):

    attribute = models.ForeignKey(Attribute, blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    time_period = models.DurationField()

    title_en = models.CharField(max_length=256)
    title_de = models.CharField(max_length=256)

    text_en = models.CharField(max_length=256)
    text_de = models.CharField(max_length=256)

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
