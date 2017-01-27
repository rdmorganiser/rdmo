from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.utils import get_uri_prefix
from apps.core.models import TranslationMixin
from apps.conditions.models import Condition


@python_2_unicode_compatible
class OptionSet(models.Model):

    uri = models.URLField(
        max_length=640, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this option set (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this option set.')
    )
    key = models.SlugField(
        max_length=128, blank=True, null=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this option set. The URI will be generated from this key.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional information about this option set.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this option set in lists.')
    )
    conditions = models.ManyToManyField(
        Condition, blank=True,
        verbose_name=_('Conditions'),
        help_text=_('The list of conditions evaluated for this option set.')
    )

    class Meta:
        ordering = ('uri', )
        verbose_name = _('Option set')
        verbose_name_plural = _('Option sets')

    def __str__(self):
        return self.uri or self.key

    def save(self, *args, **kwargs):
        self.uri = self.build_uri()
        super(OptionSet, self).save(*args, **kwargs)

        for option in self.options.all():
            option.save()

    @property
    def label(self):
        return self.key

    def build_uri(self):
        return get_uri_prefix(self) + '/options/' + self.label


@python_2_unicode_compatible
class Option(models.Model, TranslationMixin):

    uri = models.URLField(
        max_length=640, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this option (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this option.')
    )
    key = models.SlugField(
        max_length=128, blank=True, null=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this option. The URI will be generated from this key.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional information about this option.')
    )
    optionset = models.ForeignKey(
        'OptionSet', null=True, blank=True, related_name='options',
        verbose_name=_('Option set'),
        help_text=_('The option set this option belongs to.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this option in lists.')
    )
    text_en = models.CharField(
        max_length=256,
        verbose_name=_('Text (en)'),
        help_text=_('The English text displayed for this option.')
    )
    text_de = models.CharField(
        max_length=256,
        verbose_name=_('Text (de)'),
        help_text=_('The German text displayed for this option.')
    )
    additional_input = models.BooleanField(
        default=False,
        verbose_name=_('Additional input'),
        help_text=_('Designates whether an additional input is possible for this option.')
    )

    class Meta:
        ordering = ('uri', )
        verbose_name = _('Option')
        verbose_name_plural = _('Options')

    def __str__(self):
        return self.uri or self.key

    def save(self, *args, **kwargs):
        self.uri = self.build_uri()
        super(Option, self).save(*args, **kwargs)

    @property
    def label(self):
        return self.optionset.key + '/' + self.key

    @property
    def text(self):
        return self.trans('text')

    def build_uri(self):
        return get_uri_prefix(self) + '/options/' + self.label
