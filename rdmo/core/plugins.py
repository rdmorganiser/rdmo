from django.conf import settings

from .utils import import_class


class Plugin:
    label = None
    description = None

    def __init__(self, key, label, class_name):
        self.key = key
        self.label = label or self.label or key
        self.class_name = class_name

    @property
    def session(self):
        return PluginSession(self)

    def get_session_key(self, key):
        return f'{self.class_name}.{self.key}.{key}'


class PluginSession:

    def __init__(self, plugin):
        self.plugin = plugin

    @property
    def session(self):
        return self.plugin.request.session

    def get(self, key, default=None):
        session_key = self.plugin.get_session_key(key)
        return self.session.get(session_key, default)

    def set(self, key, value):
        session_key = self.plugin.get_session_key(key)
        self.session[session_key] = value

    def pop(self, key, default=None):
        session_key = self.plugin.get_session_key(key)
        return self.session.pop(session_key, default)

    def drop(self):
        # remove all keys of this plugin from the session
        prefix = self.plugin.get_session_key('')
        for session_key in [session_key for session_key in self.session.keys() if session_key.startswith(prefix)]:
            del self.session[session_key]


def get_plugins(plugin_settings):
    plugins = {}
    for key, label, class_name in getattr(settings, plugin_settings):
        plugins[key] = import_class(class_name)(key, label, class_name)
    return plugins


def get_plugin(plugin_settings, plugin_key):
    try:
        key, label, class_name = next(
            (key, label, class_name)
            for key, label, class_name in getattr(settings, plugin_settings)
            if key == plugin_key
        )
        return import_class(class_name)(key, label, class_name)
    except StopIteration:
        return None
