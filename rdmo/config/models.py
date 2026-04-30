import mimetypes
from inspect import signature

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db import models
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from rdmo.config.constants import PLUGIN_TYPES
from rdmo.config.managers import PluginManager
from rdmo.core.models import Model, TranslationMixin
from rdmo.core.utils import get_distribution_name_from_class, get_distribution_version, join_url


class Plugin(Model, TranslationMixin):

    objects = PluginManager()

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
        'questions.Catalog', blank=True,  # config app should stay below elements in hierarchy of imports
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
        verbose_name=_('Python path'),
        help_text=_('Python dotted path to the plugin class, e.g. "rdmo_plugins_provider.module.PluginClass"'),

    )
    plugin_meta = models.JSONField(
        blank=True, default=dict, editable=False,
        verbose_name=_('Plugin metadata'),
        help_text=_('Contains metadata derived from the plugin class.'),
    )
    plugin_settings = models.JSONField(
        blank=True, default=dict,
        verbose_name=_('Plugin settings'),
        help_text=_('Contains the settings for this plugin in JSON format.'),
    )
    plugin_type = models.SlugField(
        max_length=128, blank=True, default="", editable=False, choices=PLUGIN_TYPES.choices,
        verbose_name=_('Plugin type'),
        help_text=_('The type of plugin this is, e.g. "project_export".')
    )
    url_name = models.SlugField(
        max_length=128, blank=True, default="",
        verbose_name=_('URL name'),
        help_text=_('The url_name for this plugin.')
    )

    class Meta:
        ordering = ('uri', 'order')
        verbose_name = _('Plugin')
        verbose_name_plural = _('Plugins')

    def __str__(self):
        return self.uri

    def save(self, *args, **kwargs):
        self.uri = self.build_uri(self.uri_prefix, self.uri_path)

        plugin_class = self.get_plugin_class()
        self.initialize_class(plugin_class=plugin_class)
        self.plugin_type = plugin_class.plugin_type
        self.plugin_meta = self.build_plugin_meta(plugin_class)

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

    @property
    def has_search(self):
        plugin_search = self.plugin_meta.get('search')
        if plugin_search is not None:
            return plugin_search
        return getattr(self.get_plugin_class(), 'search', False)

    @property
    def has_refresh(self):
        plugin_refresh = self.plugin_meta.get('refresh')
        if plugin_refresh is not None:
            return plugin_refresh
        return getattr(self.get_plugin_class(), 'refresh', False)

    @property
    def upload_accept(self):
        plugin_accept = self.plugin_meta.get('accept')

        if isinstance(plugin_accept, dict):
            normalized_accept = {}
            for mime_type, suffixes in plugin_accept.items():
                if not isinstance(mime_type, str):
                    continue
                if not isinstance(suffixes, (list, tuple, set)):
                    continue

                normalized_suffixes = {
                    suffix for suffix in suffixes
                    if isinstance(suffix, str) and suffix.startswith('.')
                }
                if normalized_suffixes:
                    normalized_accept[mime_type] = normalized_suffixes

            return normalized_accept

        if isinstance(plugin_accept, str):
            # legacy fallback for pre 2.3.0 RDMO, e.g. `accept = '.xml'`
            suffix = plugin_accept
            mime_type, _encoding = mimetypes.guess_type(f'example{suffix}')
            if mime_type:
                return {mime_type: {suffix}}
            return {}

        if self.plugin_meta.get('upload') is True:
            # if one of the plugins does not have the accept field, but is marked as upload plugin
            # all file types are allowed
            return None

        return {}

    def get_plugin_class(self):
        return import_string(self.python_path)

    def build_plugin_meta(self, plugin_class):
        # Collect plugin metadata from class attributes.
        # Metadata is merged from the plugin class' MRO (so base class defaults are
        # included, but subclass overrides win) and only includes attributes that
        # are explicitly defined on the plugin class or its BasePlugin ancestors.
        meta = {}
        mro = plugin_class.mro()
        attrs = settings.PLUGIN_META_ATTRIBUTES

        for attr in attrs:
            if attr.startswith('distribution_'):
                continue

            if any(attr in cls.__dict__ for cls in mro):
                meta[attr] = getattr(plugin_class, attr)

        if 'distribution_name' in attrs or 'distribution_version' in attrs:
            distribution_name = get_distribution_name_from_class(plugin_class)

            if 'distribution_name' in attrs:
                meta['distribution_name'] = distribution_name

            if 'distribution_version' in attrs:
                version = get_distribution_version(distribution_name)
                meta['distribution_version'] = str(version) if version is not None else None

        return meta

    def initialize_class(self, plugin_class=None):
        cls = plugin_class or self.get_plugin_class()
        sig = signature(cls)
        if len(sig.parameters) == 0:
            return cls()
        if len(sig.parameters) == 2:
            if sig.parameters['args'].name == 'args' and sig.parameters['kwargs'].name == 'kwargs':
                return cls()
        if len(sig.parameters) == 3:  # the legacy signature, should not be called anymore
            key = self.url_name if self.url_name else self.uri_path
            return cls(key, self.title, self.python_path)
        raise ValueError(f'Could not initialize class {self.python_path} for {sig}')
