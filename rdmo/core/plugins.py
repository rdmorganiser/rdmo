from django.conf import settings

from .utils import import_class


class Plugin:

    def __init__(self, key, label, class_name):
        self.key = key
        self.label = label
        self.class_name = class_name


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
