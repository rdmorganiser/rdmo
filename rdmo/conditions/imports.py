from rdmo.core.imports import ElementImportHelper

from .serializers.v1 import ConditionSerializer
from .validators import ConditionLockedValidator, ConditionUniqueURIValidator

import_helper_condition = ElementImportHelper(
    model="conditions.condition",
    validators=(ConditionLockedValidator, ConditionUniqueURIValidator),
    foreign_fields=('source', 'target_option'),
    serializer=ConditionSerializer,
    extra_fields=('relation', 'target_text')
)
