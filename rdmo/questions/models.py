from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.cache import caches
from django.db import models
from django.utils.translation import ugettext_lazy as _

from rdmo.conditions.models import Condition
from rdmo.core.constants import VALUE_TYPE_CHOICES
from rdmo.core.models import Model, TranslationMixin
from rdmo.core.utils import get_uri_prefix
from rdmo.domain.models import Attribute

from .managers import CatalogManager, QuestionSetManager
from .validators import (CatalogUniqueKeyValidator,
                         QuestionSetUniquePathValidator,
                         QuestionUniquePathValidator,
                         SectionUniquePathValidator)


class Catalog(Model, TranslationMixin):

    objects = CatalogManager()

    uri = models.URLField(
        max_length=640, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this catalog (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this catalog.')
    )
    key = models.SlugField(
        max_length=128, blank=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this catalog.')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this catalog.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this catalog in lists.')
    )
    sites = models.ManyToManyField(
        Site, blank=True,
        verbose_name=_('Sites'),
        help_text=_('The sites this catalog belongs to (in a multi site setup).')
    )
    groups = models.ManyToManyField(
        Group, blank=True,
        verbose_name=_('Group'),
        help_text=_('The groups for which this catalog is active.')
    )
    title_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (primary)'),
        help_text=_('The title for this catalog in the primary language.')
    )
    title_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (secondary)'),
        help_text=_('The title for this catalog in the secondary language.')
    )
    title_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (tertiary)'),
        help_text=_('The title for this catalog in the tertiary language.')
    )
    title_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quaternary)'),
        help_text=_('The title for this catalog in the quaternary language.')
    )
    title_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quinary)'),
        help_text=_('The title for this catalog in the quinary language.')
    )
    help_lang1 = models.TextField(
        blank=True,
        verbose_name=_('Help (primary)'),
        help_text=_('The help text for this catalog in the primary language.')
    )
    help_lang2 = models.TextField(
        blank=True,
        verbose_name=_('Help (secondary)'),
        help_text=_('The help text for this catalog in the secondary language.')
    )
    help_lang3 = models.TextField(
        blank=True,
        verbose_name=_('Help (tertiary)'),
        help_text=_('The help text for this catalog in the tertiary language.')
    )
    help_lang4 = models.TextField(
        blank=True,
        verbose_name=_('Help (quaternary)'),
        help_text=_('The help text for this catalog in the quaternary language.')
    )
    help_lang5 = models.TextField(
        blank=True,
        verbose_name=_('Help (quinary)'),
        help_text=_('The help text for this catalog in the quinary language.')
    )

    class Meta:
        ordering = ('order',)
        verbose_name = _('Catalog')
        verbose_name_plural = _('Catalogs')

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        self.uri = get_uri_prefix(self) + '/questions/%s' % self.key
        super(Catalog, self).save(*args, **kwargs)

        for section in self.sections.all():
            section.save()

    def clean(self):
        CatalogUniqueKeyValidator(self)()

    @property
    def title(self):
        return self.trans('title')

    @property
    def help(self):
        return self.trans('help')


class Section(Model, TranslationMixin):

    uri = models.URLField(
        max_length=640, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this section (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this section.')
    )
    key = models.SlugField(
        max_length=128, blank=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this section.')
    )
    path = models.CharField(
        max_length=512, blank=True,
        verbose_name=_('Label'),
        help_text=_('The path part of the URI of this section (auto-generated).')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this section.')
    )
    catalog = models.ForeignKey(
        Catalog, on_delete=models.CASCADE, related_name='sections',
        verbose_name=_('Catalog'),
        help_text=_('The catalog this section belongs to.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('Position in lists.')
    )
    title_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (primary)'),
        help_text=_('The title for this section in the primary language.')
    )
    title_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (secondary)'),
        help_text=_('The title for this section in the secondary language.')
    )
    title_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (tertiary)'),
        help_text=_('The title for this section in the tertiary language.')
    )
    title_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quaternary)'),
        help_text=_('The title for this section in the quaternary language.')
    )
    title_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quinary)'),
        help_text=_('The title for this section in the quinary language.')
    )

    class Meta:
        ordering = ('catalog__order', 'order')
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return self.path

    def save(self, *args, **kwargs):
        self.path = Section.build_path(self.key, self.catalog)
        self.uri = get_uri_prefix(self) + '/questions/' + self.path

        super(Section, self).save(*args, **kwargs)

        for questionsets in self.questionsets.all():
            questionsets.save()

    def clean(self):
        self.path = Section.build_path(self.key, self.catalog)
        SectionUniquePathValidator(self)()

    @property
    def title(self):
        return self.trans('title')

    @classmethod
    def build_path(cls, key, catalog):
        return '%s/%s' % (catalog.key, key)


class QuestionSet(Model, TranslationMixin):

    objects = QuestionSetManager()

    uri = models.URLField(
        max_length=640, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this questionset (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this questionset.')
    )
    key = models.SlugField(
        max_length=128, blank=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this questionset.')
    )
    path = models.CharField(
        max_length=512, blank=True,
        verbose_name=_('Path'),
        help_text=_('The path part of the URI of this questionset (auto-generated).')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this questionset.')
    )
    attribute = models.ForeignKey(
        Attribute, blank=True, null=True,
        on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Attribute'),
        help_text=_('The attribute this questionset belongs to.')
    )
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name='questionsets',
        verbose_name=_('Section'),
        help_text=_('The section this questionset belongs to.')
    )
    is_collection = models.BooleanField(
        default=False,
        verbose_name=_('is collection'),
        help_text=_('Designates whether this questionset is a collection.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this questionset in lists.')
    )
    title_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (primary)'),
        help_text=_('The title for this questionset in the primary language.')
    )
    title_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (secondary)'),
        help_text=_('The title for this questionset in the secondary language.')
    )
    title_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (tertiary)'),
        help_text=_('The title for this questionset in the tertiary language.')
    )
    title_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quaternary)'),
        help_text=_('The title for this questionset in the quaternary language.')
    )
    title_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quinary)'),
        help_text=_('The title for this questionset in the quinary language.')
    )
    help_lang1 = models.TextField(
        blank=True,
        verbose_name=_('Help (primary)'),
        help_text=_('The help text for this questionset in the primary language.')
    )
    help_lang2 = models.TextField(
        blank=True,
        verbose_name=_('Help (secondary)'),
        help_text=_('The help text for this questionset in the secondary language.')
    )
    help_lang3 = models.TextField(
        blank=True,
        verbose_name=_('Help (tertiary)'),
        help_text=_('The help text for this questionset in the tertiary language.')
    )
    help_lang4 = models.TextField(
        blank=True,
        verbose_name=_('Help (quaternary)'),
        help_text=_('The help text for this questionset in the quaternary language.')
    )
    help_lang5 = models.TextField(
        blank=True,
        verbose_name=_('Help (quinary)'),
        help_text=_('The help text for this questionset in the quinary language.')
    )
    verbose_name_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (primary)'),
        help_text=_('The name displayed for this question in the primary language.')
    )
    verbose_name_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (secondary)'),
        help_text=_('The  name displayed for this question in the secondary language.')
    )
    verbose_name_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (tertiary)'),
        help_text=_('The  name displayed for this question in the tertiary language.')
    )
    verbose_name_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (quaternary)'),
        help_text=_('The  name displayed for this question in the quaternary language.')
    )
    verbose_name_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (quinary)'),
        help_text=_('The  name displayed for this question in the quinary language.')
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
    conditions = models.ManyToManyField(
        Condition, blank=True,
        verbose_name=_('Conditions'),
        help_text=_('List of conditions evaluated for this questionset.')
    )

    class Meta:
        ordering = ('section', 'order')
        verbose_name = _('Question set')
        verbose_name_plural = _('Question set')

    def __str__(self):
        return self.path

    def save(self, *args, **kwargs):
        self.path = QuestionSet.build_path(self.key, self.section)
        self.uri = get_uri_prefix(self) + '/questions/' + self.path

        super(QuestionSet, self).save(*args, **kwargs)

        for question in self.questions.all():
            question.save()

        # invalidate the cache so that changes appear instantly
        caches['api'].clear()

    def clean(self):
        self.path = QuestionSet.build_path(self.key, self.section)
        QuestionSetUniquePathValidator(self)()

    @property
    def title(self):
        return self.trans('title')

    @property
    def help(self):
        return self.trans('help')

    @property
    def verbose_name(self):
        return self.trans('verbose_name')

    @property
    def verbose_name_plural(self):
        return self.trans('verbose_name_plural')

    @classmethod
    def build_path(cls, key, section):
        return '%s/%s/%s' % (
            section.catalog.key,
            section.key,
            key
        )


class Question(Model, TranslationMixin):

    WIDGET_TYPE_CHOICES = (
        ('text', 'Text'),
        ('textarea', 'Textarea'),
        ('yesno', 'Yes/No'),
        ('checkbox', 'Checkboxes'),
        ('radio', 'Radio buttons'),
        ('select', 'Select drop-down'),
        ('range', 'Range slider'),
        ('date', 'Date picker'),
    )

    uri = models.URLField(
        max_length=640, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this question (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this question.')
    )
    key = models.SlugField(
        max_length=128, blank=True, null=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this question.')
    )
    path = models.CharField(
        max_length=512, blank=True, null=True,
        verbose_name=_('Path'),
        help_text=_('The path part of the URI of this question (auto-generated).')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this question.')
    )
    attribute = models.ForeignKey(
        Attribute, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Attribute'),
        help_text=_('The attribute this question belongs to.')
    )
    questionset = models.ForeignKey(
        QuestionSet, on_delete=models.CASCADE, related_name='questions',
        verbose_name=_('Questionset'),
        help_text=_('The question set this question belongs to.')
    )
    is_collection = models.BooleanField(
        default=False,
        verbose_name=_('is collection'),
        help_text=_('Designates whether this question is a collection.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this question in lists.')
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
        max_length=12, choices=WIDGET_TYPE_CHOICES,
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
    optionsets = models.ManyToManyField(
        'options.OptionSet', blank=True,
        verbose_name=_('Option sets'),
        help_text=_('Option sets for this question.')
    )
    conditions = models.ManyToManyField(
        Condition, blank=True,
        verbose_name=_('Conditions'),
        help_text=_('List of conditions evaluated for this question.')
    )

    class Meta:
        ordering = ('questionset', 'order')
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return self.path

    def save(self, *args, **kwargs):
        self.path = Question.build_path(self.key, self.questionset)
        self.uri = get_uri_prefix(self) + '/questions/' + self.path

        super(Question, self).save(*args, **kwargs)

        # invalidate the cache so that changes appear instantly
        caches['api'].clear()

    def clean(self):
        self.path = Question.build_path(self.key, self.questionset)
        QuestionUniquePathValidator(self)()

    @property
    def text(self):
        return self.trans('text')

    @property
    def help(self):
        return self.trans('help')

    @property
    def verbose_name(self):
        return self.trans('verbose_name')

    @property
    def verbose_name_plural(self):
        return self.trans('verbose_name_plural')

    @classmethod
    def build_path(cls, key, questionset):
        return '%s/%s/%s/%s' % (
            questionset.section.catalog.key,
            questionset.section.key,
            questionset.key,
            key
        )
