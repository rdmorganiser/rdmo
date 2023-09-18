from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from rdmo.conditions.models import Condition
from rdmo.core.models import Model, TranslationMixin
from rdmo.core.utils import join_url
from rdmo.domain.models import Attribute

from ..managers import PageManager


class Page(Model, TranslationMixin):

    objects = PageManager()

    prefetch_lookups = (
        'conditions',
        'page_questions__question__attribute',
        'page_questions__question__conditions',
        'page_questions__question__optionsets',
        'page_questionsets__questionset__attribute',
        'page_questionsets__questionset__conditions',
        'page_questionsets__questionset__questionset_questions__question__attribute',
        'page_questionsets__questionset__questionset_questions__question__conditions',
        'page_questionsets__questionset__questionset_questions__question__optionsets',
        'page_questionsets__questionset__questionset_questionsets__questionset__attribute',
        'page_questionsets__questionset__questionset_questionsets__questionset__conditions'
    )

    uri = models.URLField(
        max_length=800, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this page (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this page.')
    )
    uri_path = models.CharField(
        max_length=512, blank=True,
        verbose_name=_('URI Path'),
        help_text=_('The path for the URI of this page.')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this page.')
    )
    locked = models.BooleanField(
        default=False,
        verbose_name=_('Locked'),
        help_text=_('Designates whether this page (and its questionsets and questions) can be changed.')
    )
    attribute = models.ForeignKey(
        Attribute, blank=True, null=True, related_name='pages',
        on_delete=models.SET_NULL,
        verbose_name=_('Attribute'),
        help_text=_('The attribute this page belongs to.')
    )
    is_collection = models.BooleanField(
        default=False,
        verbose_name=_('is collection'),
        help_text=_('Designates whether this page is a collection.')
    )
    questionsets = models.ManyToManyField(
        'QuestionSet', through='PageQuestionSet', blank=True, related_name='pages',
        verbose_name=_('Question sets'),
        help_text=_('The question sets of this page.')
    )
    questions = models.ManyToManyField(
        'Question', through='PageQuestion', blank=True, related_name='pages',
        verbose_name=_('Questions'),
        help_text=_('The questions of this page.')
    )
    editors = models.ManyToManyField(
        Site, related_name='pages_as_editor', blank=True,
        verbose_name=_('Editors'),
        help_text=_('The sites that can edit this page (in a multi site setup).')
    )
    title_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (primary)'),
        help_text=_('The title for this page in the primary language.')
    )
    title_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (secondary)'),
        help_text=_('The title for this page in the secondary language.')
    )
    title_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (tertiary)'),
        help_text=_('The title for this page in the tertiary language.')
    )
    title_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quaternary)'),
        help_text=_('The title for this page in the quaternary language.')
    )
    title_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quinary)'),
        help_text=_('The title for this page in the quinary language.')
    )
    help_lang1 = models.TextField(
        blank=True,
        verbose_name=_('Help (primary)'),
        help_text=_('The help text for this page in the primary language.')
    )
    help_lang2 = models.TextField(
        blank=True,
        verbose_name=_('Help (secondary)'),
        help_text=_('The help text for this page in the secondary language.')
    )
    help_lang3 = models.TextField(
        blank=True,
        verbose_name=_('Help (tertiary)'),
        help_text=_('The help text for this page in the tertiary language.')
    )
    help_lang4 = models.TextField(
        blank=True,
        verbose_name=_('Help (quaternary)'),
        help_text=_('The help text for this page in the quaternary language.')
    )
    help_lang5 = models.TextField(
        blank=True,
        verbose_name=_('Help (quinary)'),
        help_text=_('The help text for this page in the quinary language.')
    )
    verbose_name_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (primary)'),
        help_text=_('The name displayed for this page in the primary language.')
    )
    verbose_name_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (secondary)'),
        help_text=_('The name displayed for this page in the secondary language.')
    )
    verbose_name_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (tertiary)'),
        help_text=_('The name displayed for this page in the tertiary language.')
    )
    verbose_name_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (quaternary)'),
        help_text=_('The name displayed for this page in the quaternary language.')
    )
    verbose_name_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (quinary)'),
        help_text=_('The name displayed for this page in the quinary language.')
    )
    verbose_name_plural_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (primary)'),
        help_text=_('The plural name displayed for this page in the primary language.')
    )
    verbose_name_plural_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (secondary)'),
        help_text=_('The plural name displayed for this page in the secondary language.')
    )
    verbose_name_plural_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (tertiary)'),
        help_text=_('The plural name displayed for this page in the tertiary language.')
    )
    verbose_name_plural_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (quaternary)'),
        help_text=_('The plural name displayed for this page in the quaternary language.')
    )
    verbose_name_plural_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (quinary)'),
        help_text=_('The plural name displayed for this page in the quinary language.')
    )
    conditions = models.ManyToManyField(
        Condition, blank=True, related_name='pages',
        verbose_name=_('Conditions'),
        help_text=_('List of conditions evaluated for this page.')
    )

    class Meta:
        ordering = ('uri', )
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    def __str__(self):
        return self.uri

    def save(self, *args, **kwargs):
        self.uri = self.build_uri(self.uri_prefix, self.uri_path)
        super().save(*args, **kwargs)

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

    @cached_property
    def is_locked(self):
        return self.locked or any(section.is_locked for section in self.sections.all())

    @cached_property
    def has_conditions(self):
        return self.conditions.exists()

    @cached_property
    def elements(self):
        page_elements = list(self.page_questionsets.all()) + list(self.page_questions.all())
        return [page_element.element for page_element in sorted(page_elements, key=lambda e: e.order)]

    @cached_property
    def descendants(self):
        descendants = []
        for element in self.elements:
            descendants += [element, *element.descendants]
        return descendants

    def prefetch_elements(self):
        models.prefetch_related_objects([self], *self.prefetch_lookups)

    def to_dict(self):
        return {
            'id': self.id,
            'uri': self.uri,
            'title': self.title,
            'is_collection': self.is_collection,
            'attribute': self.attribute.uri if self.attribute else None,
            'conditions': [condition.uri for condition in self.conditions.all()],
            'elements': [element.to_dict(self) for element in self.elements],
        }

    @classmethod
    def build_uri(cls, uri_prefix, uri_path):
        if not uri_path:
            raise RuntimeError('uri_path is missing')
        return join_url(uri_prefix or settings.DEFAULT_URI_PREFIX, '/questions/', uri_path)
