from rdmo.core.validators import LockedValidator, UniqueURIValidator

from .models import Task


class TaskUniqueURIValidator(UniqueURIValidator):

    model = Task


class TaskLockedValidator(LockedValidator):

    pass
