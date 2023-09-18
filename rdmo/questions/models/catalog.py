from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from rdmo.core.models import Model, TranslationMixin
from rdmo.core.utils import join_url

from ..managers import CatalogManager


class Catalog(Model, TranslationMixin):

    objects = CatalogManager()

    prefetch_lookups = (
        'catalog_sections__section',
        'catalog_sections__section__section_pages__page__attribute',
        'catalog_sections__section__section_pages__page__conditions',
        'catalog_sections__section__section_pages__page__page_questions__question__attribute',
        'catalog_sections__section__section_pages__page__page_questions__question__conditions',
        'catalog_sections__section__section_pages__page__page_questions__question__optionsets',
        'catalog_sections__section__section_pages__page__page_questionsets__questionset__attribute',
        'catalog_sections__section__section_pages__page__page_questionsets__questionset__conditions',
        'catalog_sections__section__section_pages__page__page_questionsets__questionset__questionset_questions__question__attribute',
        'catalog_sections__section__section_pages__page__page_questionsets__questionset__questionset_questions__question__conditions',
        'catalog_sections__section__section_pages__page__page_questionsets__questionset__questionset_questions__question__optionsets',
        'catalog_sections__section__section_pages__page__page_questionsets__questionset__questionset_questionsets__questionset__attribute',
        'catalog_sections__section__section_pages__page__page_questionsets__questionset__questionset_questionsets__questionset__conditions'
    )

    uri = models.URLField(
        max_length=800, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this catalog (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this catalog.')
    )
    uri_path = models.CharField(
        max_length=512, blank=True,
        verbose_name=_('URI Path'),
        help_text=_('The path for the URI of this catalog.')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this catalog.')
    )
    locked = models.BooleanField(
        default=False,
        verbose_name=_('Locked'),
        help_text=_('Designates whether this catalog (and its sections, question sets and questions) can be changed.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this catalog in lists.')
    )
    sections = models.ManyToManyField(
        'Section', through='CatalogSection', blank=True, related_name='catalogs',
        verbose_name=_('Sections'),
        help_text=_('The sections of this catalog.')
    )
    sites = models.ManyToManyField(
        Site, blank=True,
        verbose_name=_('Sites'),
        help_text=_('The sites this catalog belongs to (in a multi site setup).')
    )
    editors = models.ManyToManyField(
        Site, related_name='catalogs_as_editor', blank=True,
        verbose_name=_('Editors'),
        help_text=_('The sites that can edit this catalog (in a multi site setup).')
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
    available = models.BooleanField(
        default=True,
        verbose_name=_('Available'),
        help_text=_('Designates whether this catalog is generally available for projects.')
    )

    class Meta:
        ordering = ('uri', )
        verbose_name = _('Catalog')
        verbose_name_plural = _('Catalogs')

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

    @cached_property
    def is_locked(self):
        return self.locked

    @cached_property
    def elements(self):
        # order "in python" to not destroy prefetch
        return [element.section for element in sorted(self.catalog_sections.all(), key=lambda e: e.order)]

    @cached_property
    def descendants(self):
        descendants = []
        for element in self.elements:
            descendants += [element, *element.descendants]
        return descendants

    @cached_property
    def pages(self):
        from . import Page
        return [descendant for descendant in self.descendants if isinstance(descendant, Page)]

    @cached_property
    def questionsets(self):
        from . import QuestionSet
        return [descendant for descendant in self.descendants if isinstance(descendant, QuestionSet)]

    @cached_property
    def questions(self):
        from . import Question
        return [descendant for descendant in self.descendants if isinstance(descendant, Question)]

    def prefetch_elements(self):
        models.prefetch_related_objects([self], *self.prefetch_lookups)

    def to_dict(self):
        elements = [element.to_dict() for element in self.elements]
        return {
            'id': self.id,
            'uri': self.uri,
            'title': self.title,
            'help': self.help,
            'elements': elements,
            'sections': elements
        }

    def get_section_for_page(self, page):
        from . import Section
        try:
            return Section.objects.get(catalogs=self, pages=page)
        except (Section.DoesNotExist, Section.MultipleObjectsReturned):
            return None

    def get_prev_page(self, page):
        try:
            index = self.pages.index(page)
            return None if index == 0 else self.pages[index - 1]
        except (ValueError, IndexError):
            return None

    def get_next_page(self, page):
        try:
            index = self.pages.index(page)
            return None if index == len(self.pages) - 1 else self.pages[index + 1]
        except (ValueError, IndexError):
            return None

    @classmethod
    def build_uri(cls, uri_prefix, uri_path):
        if not uri_path:
            raise RuntimeError('uri_path is missing')
        return join_url(uri_prefix or settings.DEFAULT_URI_PREFIX, '/questions/', uri_path)
