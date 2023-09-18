from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db import models
from django.template import Context, Template
from django.utils.translation import gettext_lazy as _

from rdmo import __version__
from rdmo.core.models import TranslationMixin
from rdmo.core.utils import get_pandoc_main_version, join_url
from rdmo.questions.models import Catalog

from .managers import ViewManager
from .utils import ProjectWrapper


class View(models.Model, TranslationMixin):

    objects = ViewManager()

    uri = models.URLField(
        max_length=800, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this view (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this view.')
    )
    uri_path = models.SlugField(
        max_length=512, blank=True,
        verbose_name=_('URI Path'),
        help_text=_('The path for the URI of this view.')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this view.')
    )
    locked = models.BooleanField(
        default=False,
        verbose_name=_('Locked'),
        help_text=_('Designates whether this view can be changed.')
    )
    catalogs = models.ManyToManyField(
        Catalog, blank=True,
        verbose_name=_('Catalogs'),
        help_text=_('The catalogs this view can be used with. '
                    'An empty list implies that this view can be used with every catalog.')
    )
    sites = models.ManyToManyField(
        Site, blank=True,
        verbose_name=_('Sites'),
        help_text=_('The sites this view belongs to (in a multi site setup).')
    )
    editors = models.ManyToManyField(
        Site, related_name='views_as_editor', blank=True,
        verbose_name=_('Editors'),
        help_text=_('The sites that can edit this view (in a multi site setup).')
    )
    groups = models.ManyToManyField(
        Group, blank=True,
        verbose_name=_('Group'),
        help_text=_('The groups for which this view is active.')
    )
    template = models.TextField(
        blank=True,
        verbose_name=_('Template'),
        help_text=_('The template for this view, written in Django template language.')
    )
    title_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (primary)'),
        help_text=_('The title for this view in the primary language.')
    )
    title_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (secondary)'),
        help_text=_('The title for this view in the secondary language.')
    )
    title_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (tertiary)'),
        help_text=_('The title for this view in the tertiary language.')
    )
    title_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quaternary)'),
        help_text=_('The title for this view in the quaternary language.')
    )
    title_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quinary)'),
        help_text=_('The title for this view in the quinary language.')
    )
    help_lang1 = models.TextField(
        blank=True,
        verbose_name=_('Help (primary)'),
        help_text=_('The help text for this view in the primary language.')
    )
    help_lang2 = models.TextField(
        blank=True,
        verbose_name=_('Help (secondary)'),
        help_text=_('The help text for this view in the secondary language.')
    )
    help_lang3 = models.TextField(
        blank=True,
        verbose_name=_('Help (tertiary)'),
        help_text=_('The help text for this view in the tertiary language.')
    )
    help_lang4 = models.TextField(
        blank=True,
        verbose_name=_('Help (quaternary)'),
        help_text=_('The help text for this view in the quaternary language.')
    )
    help_lang5 = models.TextField(
        blank=True,
        verbose_name=_('Help (quinary)'),
        help_text=_('The help text for this view in the quinary language.')
    )
    available = models.BooleanField(
        default=True,
        verbose_name=_('Available'),
        help_text=_('Designates whether this view is generally available for projects.')
    )

    class Meta:
        ordering = ('uri', )
        verbose_name = _('View')
        verbose_name_plural = _('Views')

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
    def is_locked(self):
        return self.locked

    def render(self, project, snapshot=None, export_format=None):
        # render the template to a html string
        # it is important not to use models here
        site = Site.objects.get_current()
        project_wrapper = ProjectWrapper(project, snapshot)
        return Template(self.template).render(Context({
            'project': project_wrapper,
            'conditions': project_wrapper.conditions,
            'format': export_format,
            'rdmo_version': __version__,
            'site': {
                'name': site.name,
                'domain': site.domain
            },
            'pandoc_version': get_pandoc_main_version()
        }))

    @classmethod
    def build_uri(cls, uri_prefix, uri_path):
        if not uri_path:
            raise RuntimeError('uri_path is missing')
        return join_url(uri_prefix or settings.DEFAULT_URI_PREFIX, '/views/', uri_path)
