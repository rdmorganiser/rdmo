from rdmo.core.validators import LockedValidator, UniqueURIValidator

from .models import Option, OptionSet


class OptionSetUniqueURIValidator(UniqueURIValidator):

    model = OptionSet
    models = (Option, OptionSet)


class OptionUniqueURIValidator(UniqueURIValidator):

    model = Option
    models = (Option, OptionSet)


class OptionSetLockedValidator(LockedValidator):

    pass


class OptionLockedValidator(LockedValidator):

    parent_fields = ('optionsets', )
