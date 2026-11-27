from django.conf import settings

from .utils import import_class


class Plugin:
    label = None
    description = None

    def __init__(self, key, label, class_name):
        self.key = key
        self.label = label or self.label or key
        self.class_name = class_name


class PluginSession:
    '''
    Stores data for a plugin in the session of the current request, the keys are prefixed with
    the class name and the key of the plugin (or the given prefix), so that different plugins
    do not interfere:

        class ExamplePlugin(Plugin):

            @property
            def session(self):
                return PluginSession(self)
    '''

    def __init__(self, plugin, prefix=None):
        self.plugin = plugin
        self.prefix = prefix or f'{plugin.class_name}.{plugin.key}'

    @property
    def session(self):
        return self.plugin.request.session

    def get_session_key(self, key):
        return f'{self.prefix}.{key}'

    def get(self, key, default=None):
        return self.session.get(self.get_session_key(key), default)

    def set(self, key, value):
        self.session[self.get_session_key(key)] = value

    def pop(self, key, default=None):
        return self.session.pop(self.get_session_key(key), default)

    def drop(self):
        # remove all keys of this plugin from the session
        prefix = self.get_session_key('')
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
