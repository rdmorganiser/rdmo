from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from rdmo.core.validators import InstanceValidator, LockedValidator, UniqueURIValidator

from .constants import PLUGIN_TYPES
from .models import Plugin
from .utils import get_plugin_python_paths


class PluginUniqueURIValidator(UniqueURIValidator):
    model = Plugin


class PluginLockedValidator(LockedValidator):
    pass


class PluginPythonPathValidator(InstanceValidator):

    model = Plugin

    def __call__(self, data, serializer=None):
        super().__call__(data, serializer)

        available_plugin_paths = get_plugin_python_paths()
        if data.get('python_path') not in available_plugin_paths:
            self.raise_validation_error({
                'python_path': _("This path is not in the configured paths.")
            })


class PluginURLNameValidator(InstanceValidator):

    model = Plugin

    def __call__(self, data, serializer=None):
        super().__call__(data, serializer)

        plugin_class = None
        if self.instance:
            if self.instance.plugin_type:
                plugin_type = self.instance.plugin_type
            else:
                plugin_class = self.instance.get_plugin_class()
                plugin_type = plugin_class.plugin_type
        else:
            plugin_type = data.get('plugin_type')

        try:
            plugin_type = PLUGIN_TYPES(plugin_type)
        except ValueError:
            return

        if plugin_type not in (PLUGIN_TYPES.PROJECT_IMPORT, PLUGIN_TYPES.PROJECT_EXPORT):
            return

        python_path = data.get('python_path')
        if not python_path and self.instance:
            python_path = self.instance.python_path

        is_upload_plugin = False
        if self.instance and python_path == self.instance.python_path:
            is_upload_plugin = self.instance.plugin_meta.get('upload') is True
            if plugin_class is None:
                plugin_class = self.instance.get_plugin_class()
        elif python_path:
            try:
                plugin_class = import_string(python_path)
                is_upload_plugin = getattr(plugin_class, 'upload', False) is True
            except (ModuleNotFoundError, ImportError):
                is_upload_plugin = False

        if plugin_type == PLUGIN_TYPES.PROJECT_IMPORT and is_upload_plugin:
            return

        url_name = data.get('url_name')
        if url_name is None and self.instance:
            url_name = self.instance.url_name
        if url_name is None and plugin_class is not None:
            url_name = getattr(plugin_class, 'url_name', None)
        if not url_name:
            self.raise_validation_error({
                'url_name': _("This field is required for this plugin.")
            })
