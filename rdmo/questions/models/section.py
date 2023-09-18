from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from rdmo.core.models import Model, TranslationMixin
from rdmo.core.utils import join_url

from ..managers import SectionManager


class Section(Model, TranslationMixin):

    objects = SectionManager()

    prefetch_lookups = (
        'section_pages__page__attribute',
        'section_pages__page__conditions',
        'section_pages__page__page_questions__question__attribute',
        'section_pages__page__page_questions__question__conditions',
        'section_pages__page__page_questions__question__optionsets',
        'section_pages__page__page_questionsets__questionset__attribute',
        'section_pages__page__page_questionsets__questionset__conditions',
        'section_pages__page__page_questionsets__questionset__questionset_questions__question__attribute',
        'section_pages__page__page_questionsets__questionset__questionset_questions__question__conditions',
        'section_pages__page__page_questionsets__questionset__questionset_questions__question__optionsets',
        'section_pages__page__page_questionsets__questionset__questionset_questionsets__questionset__attribute',
        'section_pages__page__page_questionsets__questionset__questionset_questionsets__questionset__conditions'
    )

    uri = models.URLField(
        max_length=800, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this section (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this section.')
    )
    uri_path = models.CharField(
        max_length=512, blank=True,
        verbose_name=_('URI Path'),
        help_text=_('The path for the URI of this section.')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this section.')
    )
    locked = models.BooleanField(
        default=False,
        verbose_name=_('Locked'),
        help_text=_('Designates whether this section (and its question sets and questions) can be changed.')
    )
    pages = models.ManyToManyField(
        'Page', through='SectionPage', blank=True, related_name='sections',
        verbose_name=_('Pages'),
        help_text=_('The pages of this section.')
    )
    editors = models.ManyToManyField(
        Site, related_name='sections_as_editor', blank=True,
        verbose_name=_('Editors'),
        help_text=_('The sites that can edit this section (in a multi site setup).')
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
        ordering = ('uri', )
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return self.uri

    def save(self, *args, **kwargs):
        self.uri = self.build_uri(self.uri_prefix, self.uri_path)
        super().save(*args, **kwargs)

    @property
    def title(self):
        return self.trans('title')

    @cached_property
    def is_locked(self):
        return self.locked or any(catalog.is_locked for catalog in self.catalogs.all())

    @cached_property
    def elements(self):
        # order "in python" to not destroy prefetch
        return [element.page for element in sorted(self.section_pages.all(), key=lambda e: e.order)]

    @cached_property
    def descendants(self):
        descendants = []
        for element in self.elements:
            descendants += [element, *element.descendants]
        return descendants

    def prefetch_elements(self):
        models.prefetch_related_objects([self], *self.prefetch_lookups)

    def to_dict(self):
        elements = [element.to_dict() for element in self.elements]
        return {
            'id': self.id,
            'uri': self.uri,
            'title': self.title,
            'elements': elements,
            'pages': elements
        }

    @classmethod
    def build_uri(cls, uri_prefix, uri_path):
        if not uri_path:
            raise RuntimeError('uri_path is missing')
        return join_url(uri_prefix or settings.DEFAULT_URI_PREFIX, '/questions/', uri_path)
