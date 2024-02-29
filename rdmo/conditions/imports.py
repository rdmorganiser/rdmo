from rdmo.core.imports import ElementImportHelper

from .models import Condition
from .serializers.v1 import ConditionSerializer
from .validators import ConditionLockedValidator, ConditionUniqueURIValidator

import_helper_condition = ElementImportHelper(
    model=Condition,
    model_path="conditions.condition",
    validators=(ConditionLockedValidator, ConditionUniqueURIValidator),
    foreign_fields=('source', 'target_option'),
    serializer=ConditionSerializer,
    extra_fields=('relation', 'target_text')
)
