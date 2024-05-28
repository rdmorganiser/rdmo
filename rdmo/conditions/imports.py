from rdmo.core.import_helpers import ElementImportHelper, ExtraFieldDefaultHelper

from .models import Condition
from .validators import ConditionLockedValidator, ConditionUniqueURIValidator

import_helper_condition = ElementImportHelper(
    model=Condition,
    model_path="conditions.condition",
    validators=(ConditionLockedValidator, ConditionUniqueURIValidator),
    foreign_fields=('source', 'target_option'),
    extra_fields=(
        ExtraFieldDefaultHelper(field_name='relation', value=''),
        ExtraFieldDefaultHelper(field_name='target_text', value=''),
    ),
)
