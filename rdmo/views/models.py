from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db import models
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _
from mptt.utils import get_cached_trees

from rdmo.conditions.models import Condition
from rdmo.core.models import TranslationMixin
from rdmo.core.utils import copy_model, join_url
from rdmo.questions.models import Catalog

from .managers import ViewManager
from .utils import build_project_tree
from .validators import ViewUniqueURIValidator


class View(models.Model, TranslationMixin):

    objects = ViewManager()

    uri = models.URLField(
        max_length=640, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this view (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this view.')
    )
    key = models.SlugField(
        max_length=128, blank=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this view.')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this view.')
    )
    catalogs = models.ManyToManyField(
        Catalog, blank=True,
        verbose_name=_('Catalogs'),
        help_text=_('The catalogs this view can be used with. An empty list implies that this view can be used with every catalog.')
    )
    sites = models.ManyToManyField(
        Site, blank=True,
        verbose_name=_('Sites'),
        help_text=_('The sites this view belongs to (in a multi site setup).')
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
        ordering = ('key', )
        verbose_name = _('View')
        verbose_name_plural = _('Views')

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        self.uri = self.build_uri(self.uri_prefix, self.key)
        super().save(*args, **kwargs)

    def clean(self):
        self.uri = self.build_uri(self.uri_prefix, self.key)
        ViewUniqueURIValidator(self).validate()

    def copy(self, uri_prefix, key):
        view = copy_model(self, uri_prefix=uri_prefix, key=key)

        # copy m2m fields
        view.catalogs.set(self.catalogs.all())
        view.sites.set(self.sites.all())
        view.groups.set(self.groups.all())

        return view

    @property
    def title(self):
        return self.trans('title')

    @property
    def help(self):
        return self.trans('help')

    def render(self, project, snapshot=None):
        # render the template to a html string
        # it is important not to use models here

        descendants = project.get_descendants()
        cached_projects = get_cached_trees(descendants)
        project_tree = build_project_tree(cached_projects)

        return Template(self.template).render(Context({
            'project_id': project.id,
            'project_children': [child.id for child in cached_projects],
            'project_descendants': [descendant.id for descendant in descendants],
            'project_tree': project_tree,
            'snapshot_id': snapshot.id if snapshot else None,
            'conditions': {
                condition.key: condition.resolve(project, snapshot)
                for condition in Condition.objects.all()
            }
        }))

    @classmethod
    def build_uri(cls, uri_prefix, key):
        return join_url(uri_prefix or settings.DEFAULT_URI_PREFIX, '/views/', key)
