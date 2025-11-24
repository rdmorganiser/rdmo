from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

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

        if self.instance.available:
            try:
                import_string(data.get('python_path'))
            except (ModuleNotFoundError, ImportError):
                self.raise_validation_error({
                    'python_path': _("This path could not be not imported.")
                })
