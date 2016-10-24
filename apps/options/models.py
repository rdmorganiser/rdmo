from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.models import TranslationMixin
from apps.domain.models import Attribute


@python_2_unicode_compatible
class OptionSet(models.Model):

    attribute = models.ForeignKey(Attribute, null=True, blank=True, related_name='optionsets')

    title = models.CharField(max_length=256, validators=[
        RegexValidator('^[a-zA-z0-9_]*$', _('Only letters, numbers, or underscores are allowed.'))
    ])

    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('attribute', 'order', )
        verbose_name = _('OptionSet')
        verbose_name_plural = _('OptionSets')

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Option(models.Model, TranslationMixin):

    optionset = models.ForeignKey('OptionSet', null=True, blank=True, related_name='options')

    title = models.CharField(max_length=256, validators=[
        RegexValidator('^[a-zA-z0-9_]*$', _('Only letters, numbers, or underscores are allowed.'))
    ])

    order = models.IntegerField(default=0)

    text_en = models.CharField(max_length=256)
    text_de = models.CharField(max_length=256)

    additional_input = models.BooleanField(default=False)

    class Meta:
        ordering = ('optionset', 'order', )
        verbose_name = _('Option')
        verbose_name_plural = _('Options')

    def __str__(self):
        return self.title

    @property
    def text(self):
        return self.trans('text')
