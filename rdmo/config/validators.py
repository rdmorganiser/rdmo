from rdmo.core.validators import LockedValidator, UniqueURIValidator

from .models import Plugin


class PluginUniqueURIValidator(UniqueURIValidator):
    model = Plugin


class PluginLockedValidator(LockedValidator):
    pass
