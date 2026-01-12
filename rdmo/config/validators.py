from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from rdmo.core.utils import get_plugin_python_paths
from rdmo.core.validators import InstanceValidator, LockedValidator, UniqueURIValidator

from .constants import PLUGIN_TYPES
from .models import Plugin
from .utils import get_plugin_type_from_class


class PluginUniqueURIValidator(UniqueURIValidator):
    model = Plugin


class PluginLockedValidator(LockedValidator):
    pass


class PluginPythonPathValidator(InstanceValidator):

    model = Plugin

    def __call__(self, data, serializer=None):
        super().__call__(data, serializer)

        available_plugin_paths = get_plugin_python_paths()
        if not available_plugin_paths:
            self.raise_validation_error({
                'python_path': _("There are no python paths for plugins available.")
            })

        if data.get('python_path') not in available_plugin_paths:
            self.raise_validation_error({
                'python_path': _("This path is not in the configured paths.")
            })

        if self.instance and self.instance.available:
            try:  # a double-check, maybe not needed
                import_string(data.get('python_path'))
            except (ModuleNotFoundError, ImportError):
                self.raise_validation_error({
                    'python_path': _("This path could not be not imported.")
                })


class PluginURLNameValidator(InstanceValidator):

    model = Plugin

    def __call__(self, data, serializer=None):
        super().__call__(data, serializer)

        if self.instance:
            if self.instance.plugin_type:
                plugin_type = self.instance.plugin_type
            else:
                plugin_type = get_plugin_type_from_class(self.instance.get_class())
        else:
            plugin_type = data.get('plugin_type')

        try:
            plugin_type = PLUGIN_TYPES(plugin_type)
        except ValueError:
            return

        if plugin_type == PLUGIN_TYPES.PROJECT_IMPORT:
            url_name = data.get('url_name')
            if url_name is None and self.instance:
                url_name = self.instance.url_name
            if not url_name:
                self.raise_validation_error({
                    'url_name': _("This field is required for project import plugins.")
                })
