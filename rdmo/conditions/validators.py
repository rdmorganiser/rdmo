from rdmo.core.validators import LockedValidator, UniqueURIValidator

from .models import Condition


class ConditionUniqueURIValidator(UniqueURIValidator):

    model = Condition


class ConditionLockedValidator(LockedValidator):

    pass
