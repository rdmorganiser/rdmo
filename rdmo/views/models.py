from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db import models
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _

from rdmo.conditions.models import Condition
from rdmo.core.models import TranslationMixin
from rdmo.core.utils import get_uri_prefix
from rdmo.questions.models import Catalog

from .managers import ViewManager
from .validators import ViewUniqueKeyValidator


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

    class Meta:
        ordering = ('key', )
        verbose_name = _('View')
        verbose_name_plural = _('Views')

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        self.uri = self.build_uri()
        super(View, self).save(*args, **kwargs)

    def clean(self):
        ViewUniqueKeyValidator(self).validate()

    @property
    def title(self):
        return self.trans('title')

    @property
    def help(self):
        return self.trans('help')

    def build_uri(self):
        return get_uri_prefix(self) + '/views/' + self.key

    def render(self, project, snapshot=None):
        # # get list of conditions
        conditions = {}
        for condition in Condition.objects.all():
            conditions[condition.key] = condition.resolve(project, snapshot)

        # get all values for this snapshot and put them in a dict labled by the values attibute path
        values = {}
        for value in project.values.filter(snapshot=snapshot):
            if value.attribute:
                attribute_path = value.attribute.path
                set_index = value.set_index

                # create entry for this values attribute in the values_dict
                if attribute_path not in values:
                    values[attribute_path] = []

                # add this value to the values
                try:
                    values[attribute_path][set_index].append(value)
                except IndexError:
                    values[attribute_path].append([value])

        # render the template to a html string
        return Template(self.template).render(Context({
            'conditions': conditions,
            'values': values
        }))
