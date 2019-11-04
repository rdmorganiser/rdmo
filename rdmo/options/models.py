from django.db import models
from django.utils.translation import ugettext_lazy as _

from rdmo.core.utils import get_uri_prefix
from rdmo.core.models import TranslationMixin
from rdmo.conditions.models import Condition

from .validators import OptionSetUniqueKeyValidator, OptionUniquePathValidator


class OptionSet(models.Model):

    uri = models.URLField(
        max_length=640, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this option set (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this option set.')
    )
    key = models.SlugField(
        max_length=128, blank=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this option set.')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this option set.')
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
        return self.key

    def save(self, *args, **kwargs):
        self.uri = get_uri_prefix(self) + '/options/' + self.label
        super(OptionSet, self).save(*args, **kwargs)

        for option in self.options.all():
            option.save()

    def clean(self):
        OptionSetUniqueKeyValidator(self).validate()

    @property
    def label(self):
        return self.key


class Option(models.Model, TranslationMixin):

    uri = models.URLField(
        max_length=640, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this option (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this option.')
    )
    key = models.SlugField(
        max_length=128, blank=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this option.')
    )
    path = models.SlugField(
        max_length=512, blank=True,
        verbose_name=_('Path'),
        help_text=_('The path part of the URI for this option (auto-generated).')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this option.')
    )
    optionset = models.ForeignKey(
        'OptionSet', on_delete=models.CASCADE, related_name='options',
        verbose_name=_('Option set'),
        help_text=_('The option set this option belongs to.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('Position in lists.')
    )
    text_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (primary)'),
        help_text=_('The text for this option in the primary language.')
    )
    text_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (secondary)'),
        help_text=_('The text for this option in the secondary language.')
    )
    text_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (tertiary)'),
        help_text=_('The text for this option in the tertiary language.')
    )
    text_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (quaternary)'),
        help_text=_('The text for this option in the quaternary language.')
    )
    text_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (quinary)'),
        help_text=_('The text for this option in the quinary language.')
    )
    additional_input = models.BooleanField(
        default=False,
        verbose_name=_('Additional input'),
        help_text=_('Designates whether an additional input is possible for this option.')
    )

    class Meta:
        ordering = ('optionset__order', 'optionset__key', 'order', 'key')
        verbose_name = _('Option')
        verbose_name_plural = _('Options')

    def __str__(self):
        return self.path

    def save(self, *args, **kwargs):
        self.path = Option.build_path(self.key, self.optionset)
        self.uri = get_uri_prefix(self) + '/options/' + self.path

        super(Option, self).save(*args, **kwargs)

    def clean(self):
        self.path = Option.build_path(self.key, self.optionset)
        OptionUniquePathValidator(self)()

    @property
    def text(self):
        return self.trans('text')

    @property
    def label(self):
        return '%s ("%s")' % (self.path, self.text)

    @classmethod
    def build_path(cls, key, optionset):
        return '%s/%s' % (optionset.key, key) if (optionset and key) else None
