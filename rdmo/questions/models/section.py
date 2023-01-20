from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from rdmo.core.models import Model, TranslationMixin
from rdmo.core.utils import copy_model, join_url


class Section(Model, TranslationMixin):

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
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('Position in lists.')
    )
    pages = models.ManyToManyField(
        'Page', blank=True, related_name='sections',
        verbose_name=_('Pages'),
        help_text=_('The pages of this section.')
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

        for page in self.pages.all():
            page.save()

    def copy(self, uri_prefix, uri_path):
        section = copy_model(self, uri_prefix=uri_prefix, uri_path=uri_path)

        # copy m2m fields
        section.pages.set(self.pages.all())

        return section

    @property
    def parent_fields(self):
        return ('catalog', )

    @property
    def title(self):
        return self.trans('title')

    @property
    def is_locked(self):
        return self.locked or any([catalog.is_locked for catalog in self.catalogs.all()])

    def get_descendants(self, include_self=False):
        # this function tries to mimic the same function from mptt
        descendants = [self] if include_self else []
        for page in self.pages.all():
            descendants += page.get_descendants(include_self=True)
        return descendants

    @classmethod
    def build_uri(cls, uri_prefix, uri_path):
        if not uri_path:
            raise RuntimeError('uri_path is missing')
        return join_url(uri_prefix or settings.DEFAULT_URI_PREFIX, '/questions/', uri_path)
