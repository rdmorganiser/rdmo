from rdmo.core.validators import LockedValidator, UniqueURIValidator

from .models import View


class ViewUniqueURIValidator(UniqueURIValidator):

    model = View


class ViewLockedValidator(LockedValidator):

    pass
