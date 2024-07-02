from rdmo.core.import_helpers import ElementImportHelper, ExtraFieldHelper

from .models import Condition
from .validators import ConditionLockedValidator, ConditionUniqueURIValidator

import_helper_condition = ElementImportHelper(
    model=Condition,
    validators=(ConditionLockedValidator, ConditionUniqueURIValidator),
    foreign_fields=('source', 'target_option'),
    extra_fields=(
        ExtraFieldHelper(field_name='relation', value=''),
        ExtraFieldHelper(field_name='target_text', value=''),
    ),
)
