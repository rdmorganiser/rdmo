from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from rdmo.conditions.models import Condition
from rdmo.core.constants import VALUE_TYPE_CHOICES
from rdmo.core.models import Model, TranslationMixin
from rdmo.core.utils import join_url
from rdmo.domain.models import Attribute
from rdmo.options.models import Option

from ..managers import QuestionManager


class Question(Model, TranslationMixin):

    objects = QuestionManager()

    prefetch_lookups = (
        'conditions',
        'optionsets'
    )

    uri = models.URLField(
        max_length=800, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this question (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this question.')
    )
    uri_path = models.CharField(
        max_length=512, blank=True, null=True,
        verbose_name=_('URI Path'),
        help_text=_('The path for the URI of this question.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this question.')
    )
    locked = models.BooleanField(
        default=False,
        verbose_name=_('Locked'),
        help_text=_('Designates whether this question can be changed.')
    )
    attribute = models.ForeignKey(
        Attribute, blank=True, null=True, on_delete=models.SET_NULL, related_name='questions',
        verbose_name=_('Attribute'),
        help_text=_('The attribute this question belongs to.')
    )
    is_collection = models.BooleanField(
        default=False,
        verbose_name=_('is collection'),
        help_text=_('Designates whether this question is a collection.')
    )
    is_optional = models.BooleanField(
        default=False,
        verbose_name=_('is optional'),
        help_text=_('Designates whether this question is optional.')
    )
    editors = models.ManyToManyField(
        Site, related_name='questions_as_editor', blank=True,
        verbose_name=_('Editors'),
        help_text=_('The sites that can edit this question (in a multi site setup).')
    )
    help_lang1 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Help (primary)'),
        help_text=_('The help text for this question in the primary language.')
    )
    help_lang2 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Help (secondary)'),
        help_text=_('The help text for this question in the secondary language.')
    )
    help_lang3 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Help (tertiary)'),
        help_text=_('The help text for this question in the tertiary language.')
    )
    help_lang4 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Help (quaternary)'),
        help_text=_('The help text for this question in the quaternary language.')
    )
    help_lang5 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Help (quinary)'),
        help_text=_('The help text for this question in the quinary language.')
    )
    text_lang1 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Text (primary)'),
        help_text=_('The text for this question in the primary language.')
    )
    text_lang2 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Text (secondary)'),
        help_text=_('The text for this question in the secondary language.')
    )
    text_lang3 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Text (tertiary)'),
        help_text=_('The text for this question in the tertiary language.')
    )
    text_lang4 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Text (quaternary)'),
        help_text=_('The text for this question in the quaternary language.')
    )
    text_lang5 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Text (quinary)'),
        help_text=_('The text for this question in the quinary language.')
    )
    default_text_lang1 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Default text value (primary)'),
        help_text=_('The default text value for this question in the primary language.')
    )
    default_text_lang2 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Default text value (secondary)'),
        help_text=_('The default text value for this question in the secondary language.')
    )
    default_text_lang3 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Default text value (tertiary)'),
        help_text=_('The default text value for this question in the tertiary language.')
    )
    default_text_lang4 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Default text value (quaternary)'),
        help_text=_('The default text value for this question in the quaternary language.')
    )
    default_text_lang5 = models.TextField(
        null=True, blank=True,
        verbose_name=_('Default text value (quinary)'),
        help_text=_('The default text value for this question in the quinary language.')
    )
    default_option = models.ForeignKey(
        Option, blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name=_('Default option'),
        help_text=_('The default option for this question. To be used with regular optionsets.')
    )
    default_external_id = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Default external id'),
        help_text=_('The default external id for this question. To be used with dynamic optionsets.')
    )
    verbose_name_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (primary)'),
        help_text=_('The name displayed for this question in the primary language.')
    )
    verbose_name_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (secondary)'),
        help_text=_('The name displayed for this question in the secondary language.')
    )
    verbose_name_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (tertiary)'),
        help_text=_('The name displayed for this question in the tertiary language.')
    )
    verbose_name_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (quaternary)'),
        help_text=_('The name displayed for this question in the quaternary language.')
    )
    verbose_name_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (quinary)'),
        help_text=_('The name displayed for this question in the quinary language.')
    )
    verbose_name_plural_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (primary)'),
        help_text=_('The plural name displayed for this question in the primary language.')
    )
    verbose_name_plural_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (secondary)'),
        help_text=_('The plural name displayed for this question in the secondary language.')
    )
    verbose_name_plural_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (tertiary)'),
        help_text=_('The plural name displayed for this question in the tertiary language.')
    )
    verbose_name_plural_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (quaternary)'),
        help_text=_('The plural name displayed for this question in the quaternary language.')
    )
    verbose_name_plural_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (quinary)'),
        help_text=_('The plural name displayed for this question in the quinary language.')
    )
    widget_type = models.CharField(
        max_length=16,
        verbose_name=_('Widget type'),
        help_text=_('Type of widget for this question.')
    )
    value_type = models.CharField(
        max_length=8, choices=VALUE_TYPE_CHOICES,
        verbose_name=_('Value type'),
        help_text=_('Type of value for this question.')
    )
    minimum = models.FloatField(
        null=True, blank=True,
        verbose_name=_('Minimum'),
        help_text=_('Minimal value for this question.')
    )
    maximum = models.FloatField(
        null=True, blank=True,
        verbose_name=_('Maximum'),
        help_text=_('Maximum value for this question.')
    )
    step = models.FloatField(
        null=True, blank=True,
        verbose_name=_('Step'),
        help_text=_('Step in which the value for this question can be incremented/decremented.')
    )
    unit = models.CharField(
        max_length=64, blank=True,
        verbose_name=_('Unit'),
        help_text=_('Unit for this question.')
    )
    width = models.IntegerField(
        null=True, blank=True,
        verbose_name=_('Width'),
        help_text=_('Width for the widget of this question (optional, full width: 12).')
    )
    optionsets = models.ManyToManyField(
        'options.OptionSet', blank=True, related_name='questions',
        verbose_name=_('Option sets'),
        help_text=_('Option sets for this question.')
    )
    conditions = models.ManyToManyField(
        Condition, blank=True, related_name='questions',
        verbose_name=_('Conditions'),
        help_text=_('List of conditions evaluated for this question.')
    )

    class Meta:
        ordering = ('uri', )
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return self.uri

    def save(self, *args, **kwargs):
        self.uri = self.build_uri(self.uri_prefix, self.uri_path)
        super().save(*args, **kwargs)

    @property
    def text(self):
        return self.trans('text')

    @property
    def help(self):
        return self.trans('help')

    @property
    def default_text(self):
        return self.trans('default_text')

    @property
    def verbose_name(self):
        return self.trans('verbose_name')

    @property
    def verbose_name_plural(self):
        return self.trans('verbose_name_plural')

    @cached_property
    def is_locked(self):
        return self.locked or \
            any(page.is_locked for page in self.pages.all()) or \
            any(questionset.is_locked for questionset in self.questionsets.all())

    @cached_property
    def has_conditions(self):
        return self.conditions.exists()

    @cached_property
    def descendants(self):
        return []

    def prefetch_elements(self):
        models.prefetch_related_objects([self], *self.prefetch_lookups)

    def to_dict(self, *ancestors):
        return {
            'id': self.id,
            'uri': self.uri,
            'text': self.text,
            'is_collection': self.is_collection,
            'attribute': self.attribute.uri if self.attribute else None,
            'ancestors': [{
                'id': ancestor.id,
                'is_collection': ancestor.is_collection,
                'verbose_name': ancestor.verbose_name,
                'attribute': ancestor.attribute.uri if ancestor.attribute else None,
                'conditions': [condition.uri for condition in ancestor.conditions.all()]
            } for ancestor in ancestors],
            'conditions': [condition.uri for condition in self.conditions.all()]
        }

    @classmethod
    def build_uri(cls, uri_prefix, uri_path):
        if not uri_path:
            raise RuntimeError('uri_path is missing')
        return join_url(uri_prefix or settings.DEFAULT_URI_PREFIX, '/questions/', uri_path)
