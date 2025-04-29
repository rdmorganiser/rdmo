from __future__ import annotations

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from rdmo.conditions.models import Condition
from rdmo.core.models import TranslationMixin
from rdmo.core.plugins import get_plugin
from rdmo.core.utils import join_url


class OptionSet(models.Model):

    uri = models.URLField(
        max_length=800, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this option set (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this option set.')
    )
    uri_path = models.CharField(
        max_length=512, blank=True,
        verbose_name=_('URI Path'),
        help_text=_('The path for the URI of this option set.')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this option set.')
    )
    locked = models.BooleanField(
        default=False,
        verbose_name=_('Locked'),
        help_text=_('Designates whether this option set (and its options) can be changed.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this option set in lists.')
    )
    editors = models.ManyToManyField(
        Site, related_name='optionsets_as_editor', blank=True,
        verbose_name=_('Editors'),
        help_text=_('The sites that can edit this option set (in a multi site setup).')
    )
    provider_key = models.SlugField(
        max_length=128, blank=True,
        verbose_name=_('Provider'),
        help_text=_('The provider for this optionset. If set, it will create dynamic options for this optionset.')
    )
    options = models.ManyToManyField(
        'Option', through='OptionSetOption', blank=True, related_name='optionsets',
        verbose_name=_('Options'),
        help_text=_('The list of options for this option set.')
    )
    conditions = models.ManyToManyField(
        Condition, blank=True, related_name='optionsets',
        verbose_name=_('Conditions'),
        help_text=_('The list of conditions evaluated for this option set.')
    )

    class Meta:
        ordering = ('uri', )
        verbose_name = _('Option set')
        verbose_name_plural = _('Option sets')

    def __str__(self):
        return self.uri

    def save(self, *args, **kwargs):
        self.uri = self.build_uri(self.uri_prefix, self.uri_path)
        super().save(*args, **kwargs)

    @property
    def label(self) -> str:
        return self.uri

    @property
    def provider(self) -> list:
        return get_plugin('OPTIONSET_PROVIDERS', self.provider_key)

    @property
    def has_provider(self) -> bool:
        return self.provider is not None

    @property
    def has_search(self) -> bool:
        return self.has_provider and self.provider.search

    @property
    def has_refresh(self) -> bool:
        return self.has_provider and self.provider.refresh

    @property
    def has_conditions(self) -> bool:
        return self.conditions.exists()

    @property
    def is_locked(self) -> bool:
        return self.locked

    @cached_property
    def elements(self) -> list[Option]:
        return [element.option for element in sorted(self.optionset_options.all(), key=lambda e: e.order)]

    @classmethod
    def build_uri(cls, uri_prefix, uri_path):
        if not uri_path:
            raise RuntimeError('uri_path is missing')
        return join_url(uri_prefix or settings.DEFAULT_URI_PREFIX, '/options/', uri_path)


class OptionSetOption(models.Model):

    optionset = models.ForeignKey(
        'OptionSet', on_delete=models.CASCADE, related_name='optionset_options'
    )
    option = models.ForeignKey(
        'Option', on_delete=models.CASCADE, related_name='option_optionsets'
    )
    order = models.IntegerField(
        default=0
    )

    class Meta:
        ordering = ('optionset', 'order')

    def __str__(self):
        return f'{self.optionset} / {self.option} [{self.order}]'


class Option(models.Model, TranslationMixin):

    ADDITIONAL_INPUT_NONE = ''
    ADDITIONAL_INPUT_TEXT = 'text'
    ADDITIONAL_INPUT_TEXTAREA = 'textarea'
    ADDITIONAL_INPUT_CHOICES = (
        (ADDITIONAL_INPUT_NONE, '---------'),
        (ADDITIONAL_INPUT_TEXT, _('Text')),
        (ADDITIONAL_INPUT_TEXTAREA, _('Textarea'))
    )

    uri = models.URLField(
        max_length=800, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this option (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this option.')
    )
    uri_path = models.CharField(
        max_length=512, blank=True,
        verbose_name=_('URI Path'),
        help_text=_('The path for the URI of this option.')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this option.')
    )
    locked = models.BooleanField(
        default=False,
        verbose_name=_('Locked'),
        help_text=_('Designates whether this option can be changed.')
    )
    editors = models.ManyToManyField(
        Site, related_name='options_as_editor', blank=True,
        verbose_name=_('Editors'),
        help_text=_('The sites that can edit this option (in a multi site setup).')
    )
    text_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (primary)'),
        help_text=_('The text for this option (in the primary language).')
    )
    text_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (secondary)'),
        help_text=_('The text for this option (in the secondary language).')
    )
    text_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (tertiary)'),
        help_text=_('The text for this option (in the tertiary language).')
    )
    text_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (quaternary)'),
        help_text=_('The text for this option (in the quaternary language).')
    )
    text_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (quinary)'),
        help_text=_('The text for this option (in the quinary language).')
    )
    help_lang1 = models.TextField(
        blank=True, default="",
        verbose_name=_('Help (primary)'),
        help_text=_('The help text for this option (in the primary language).')
    )
    help_lang2 = models.TextField(
        blank=True, default="",
        verbose_name=_('Help (secondary)'),
        help_text=_('The help text for this option (in the secondary language).')
    )
    help_lang3 = models.TextField(
        blank=True, default="",
        verbose_name=_('Help (tertiary)'),
        help_text=_('The help text for this option (in the tertiary language).')
    )
    help_lang4 = models.TextField(
        blank=True, default="",
        verbose_name=_('Help (quaternary)'),
        help_text=_('The help text for this option (in the quaternary language).')
    )
    help_lang5 = models.TextField(
        blank=True, default="",
        verbose_name=_('Help (quinary)'),
        help_text=_('The help text for this option (in the quinary language).')
    )
    default_text_lang1 = models.TextField(
        blank=True, default="",
        verbose_name=_('Default text value (primary)'),
        help_text=_('The default text value for the additional input of this option (in the primary language).')
    )
    default_text_lang2 = models.TextField(
        blank=True, default="",
        verbose_name=_('Default text value (secondary)'),
        help_text=_('The default text value for the additional input of this option (in the secondary language).')
    )
    default_text_lang3 = models.TextField(
        blank=True, default="",
        verbose_name=_('Default text value (tertiary)'),
        help_text=_('The default text value for the additional input of this option (in the tertiary language).')
    )
    default_text_lang4 = models.TextField(
        blank=True, default="",
        verbose_name=_('Default text value (quaternary)'),
        help_text=_('The default text value for the additional input of this option (in the quaternary language).')
    )
    default_text_lang5 = models.TextField(
        blank=True, default="",
        verbose_name=_('Default text value (quinary)'),
        help_text=_('The default text value for the additional input of this option (in the quinary language).')
    )
    view_text_lang1 = models.TextField(
        blank=True, default="",
        verbose_name=_('View text (primary)'),
        help_text=_('The view text for this option (in the primary language).')
    )
    view_text_lang2 = models.TextField(
        blank=True, default="",
        verbose_name=_('View text (secondary)'),
        help_text=_('The view text for this option (in the secondary language).')
    )
    view_text_lang3 = models.TextField(
        blank=True, default="",
        verbose_name=_('View text (tertiary)'),
        help_text=_('The view text for this option (in the tertiary language).')
    )
    view_text_lang4 = models.TextField(
        blank=True, default="",
        verbose_name=_('View text (quaternary)'),
        help_text=_('The view text for this option (in the quaternary language).')
    )
    view_text_lang5 = models.TextField(
        blank=True, default="",
        verbose_name=_('View text (quinary)'),
        help_text=_('The view text for this option (in the quinary language).')
    )
    additional_input = models.CharField(
        max_length=256, blank=True, default=ADDITIONAL_INPUT_NONE, choices=ADDITIONAL_INPUT_CHOICES,
        verbose_name=_('Additional input'),
        help_text=_('Designates whether an additional input is possible for this option.')
    )

    class Meta:
        ordering = ('uri', )
        verbose_name = _('Option')
        verbose_name_plural = _('Options')

    def __str__(self):
        return self.uri

    def save(self, *args, **kwargs):
        self.uri = self.build_uri(self.uri_prefix, self.uri_path)
        super().save(*args, **kwargs)

    @property
    def text(self) -> str:
        return self.trans('text')

    @property
    def help(self) -> str:
        return self.trans('help')

    @property
    def default_text(self) -> str:
        return self.trans('default_text')

    @property
    def view_text(self) -> str:
        return self.trans('view_text')

    @property
    def text_and_help(self) -> str:
        return f'{self.text} [{self.help}]' if self.help else self.text

    @property
    def label(self) -> str:
        return f'{self.uri} ("{self.text}")'

    @property
    def is_locked(self) -> bool:
        return self.locked or self.optionsets.filter(locked=True).exists()

    @classmethod
    def build_uri(cls, uri_prefix, uri_path):
        if not uri_path:
            raise RuntimeError('uri_path is missing')
        return join_url(uri_prefix or settings.DEFAULT_URI_PREFIX, '/options/', uri_path)
