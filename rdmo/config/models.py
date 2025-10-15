from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _

from rdmo.core.models import Model, TranslationMixin
from rdmo.core.utils import join_url
from rdmo.questions.models import Catalog


class Plugin(Model, TranslationMixin):

    uri = models.URLField(
        max_length=800, blank=True, default="",
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this plugin (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this plugin.')
    )
    uri_path = models.CharField(
        max_length=512, blank=True, default="",
        verbose_name=_('URI Path'),
        help_text=_('The path for the URI of this plugin.')
    )
    comment = models.TextField(
        blank=True, default="",
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this question.')
    )
    locked = models.BooleanField(
        default=False,
        verbose_name=_('Locked'),
        help_text=_('Designates whether this plugin can be changed.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this plugin in lists.')
    )
    sites = models.ManyToManyField(
        Site, blank=True,
        verbose_name=_('Sites'),
        help_text=_('The sites this plugin belongs to (in a multi site setup).')
    )
    editors = models.ManyToManyField(
        Site, related_name='plugins_as_editor', blank=True,
        verbose_name=_('Editors'),
        help_text=_('The sites that can edit this plugin (in a multi site setup).')
    )
    groups = models.ManyToManyField(
        Group, blank=True,
        verbose_name=_('Group'),
        help_text=_('The groups for which this plugin is active.')
    )
    catalogs = models.ManyToManyField(
        Catalog, blank=True,
        verbose_name=_('Catalogs'),
        help_text=_('The catalogs this plugin can be used with. '
                    'An empty list implies that this plugin can be used with every catalog.')
    )
    title_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (primary)'),
        help_text=_('The title for this plugin (in the primary language).')
    )
    title_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (secondary)'),
        help_text=_('The title for this plugin (in the secondary language).')
    )
    title_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (tertiary)'),
        help_text=_('The title for this plugin (in the tertiary language).')
    )
    title_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quaternary)'),
        help_text=_('The title for this plugin (in the quaternary language).')
    )
    title_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quinary)'),
        help_text=_('The title for this plugin (in the quinary language).')
    )
    help_lang1 = models.TextField(
        blank=True,
        verbose_name=_('Help (primary)'),
        help_text=_('The help text for this plugin (in the primary language).')
    )
    help_lang2 = models.TextField(
        blank=True,
        verbose_name=_('Help (secondary)'),
        help_text=_('The help text for this plugin (in the secondary language).')
    )
    help_lang3 = models.TextField(
        blank=True,
        verbose_name=_('Help (tertiary)'),
        help_text=_('The help text for this plugin (in the tertiary language).')
    )
    help_lang4 = models.TextField(
        blank=True,
        verbose_name=_('Help (quaternary)'),
        help_text=_('The help text for this plugin (in the quaternary language).')
    )
    help_lang5 = models.TextField(
        blank=True,
        verbose_name=_('Help (quinary)'),
        help_text=_('The help text for this plugin (in the quinary language).')
    )
    available = models.BooleanField(
        default=True,
        verbose_name=_('Available'),
        help_text=_('Designates whether this plugin is generally available for projects.')
    )
    python_path = models.CharField(
        max_length=512,
        verbose_name=_("Python path"),
        help_text=_("Python dotted path to the plugin class, e.g. 'rdmo_specific_plugin.module.PluginClass'"),

    )
    plugin_settings = models.JSONField(
        blank=True, default=dict,
        verbose_name=_("Plugin settings"),
        help_text=_("Contains the settings for this plugin in JSON format."),
    )

    class Meta:
        ordering = ('uri', )
        verbose_name = _('Plugin')
        verbose_name_plural = _('Plugins')

    def __str__(self):
        return self.uri

    def save(self, *args, **kwargs):
        self.uri = self.build_uri(self.uri_prefix, self.uri_path)
        super().save(*args, **kwargs)

    @property
    def title(self) -> str:
        return self.trans('title')

    @property
    def help(self) -> str:
        return self.trans('help')

    @property
    def is_locked(self):
        return self.locked

    @classmethod
    def build_uri(cls, uri_prefix, uri_path):
        if not uri_path:
            raise RuntimeError('uri_path is missing')
        return join_url(uri_prefix or settings.DEFAULT_URI_PREFIX, '/plugins/', uri_path)
