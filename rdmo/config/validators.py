from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from rdmo.core.utils import get_plugin_python_paths
from rdmo.core.validators import InstanceValidator, LockedValidator, UniqueURIValidator

from .models import Plugin


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
