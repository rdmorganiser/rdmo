from rdmo.config.utils import PLUGIN_SETTING_MISSING, get_plugin_django_setting


class PluginSettings:

    def __init__(self, plugin_instance):
        self.plugin_instance = plugin_instance

    @property
    def plugin(self):
        return self.plugin_instance.plugin

    @property
    def plugin_settings(self):
        if self.plugin is None:
            return {}
        if isinstance(self.plugin.plugin_settings, dict):
            return self.plugin.plugin_settings
        return {}

    @property
    def settings_form_class(self):
        return self.plugin_instance.settings_form_class

    @property
    def form_fields(self):
        if self.settings_form_class is None:
            return None
        return self.settings_form_class.base_fields

    def __getattr__(self, name):
        if self.form_fields is not None and name not in self.form_fields:
            raise AttributeError(f'{name} is not a setting for this plugin.')

        if name in self.plugin_settings:
            return self.plugin_settings[name]

        django_setting = get_plugin_django_setting(self.plugin_instance, name)
        if django_setting is not PLUGIN_SETTING_MISSING:
            return django_setting

        settings_defaults = getattr(self.plugin_instance, 'settings_defaults', {}) or {}
        if name in settings_defaults:
            return settings_defaults[name]

        if self.form_fields is not None:
            return self.form_fields[name].initial

        raise AttributeError(f'{name} is not a setting for this plugin.')

    def get(self, name, default=None):
        try:
            return getattr(self, name)
        except AttributeError:
            return default


class BasePlugin:

    plugin = None
    settings_defaults = {}
    settings_form_class = None
    settings_namespace = None

    @property
    def plugin_settings(self):
        if self.plugin is None:
            return {}
        return self.plugin.plugin_settings or {}

    @property
    def plugin_metadata(self):
        if self.plugin is None:
            return {}
        return self.plugin.plugin_meta or {}

    @property
    def settings(self):
        return PluginSettings(self)
