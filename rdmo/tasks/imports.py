from rdmo.core.import_helpers import ElementImportHelper, ExtraFieldDefaultHelper

from .models import Task
from .validators import TaskLockedValidator, TaskUniqueURIValidator

import_helper_task = ElementImportHelper(
    model=Task,
    model_path="tasks.task",
    validators=(TaskLockedValidator, TaskUniqueURIValidator),
    lang_fields=('title', 'text'),
    foreign_fields=('start_attribute', 'end_attribute'),
    extra_fields=(
        ExtraFieldDefaultHelper(field_name='order'),
        ExtraFieldDefaultHelper(field_name='days_before'),
        ExtraFieldDefaultHelper(field_name='days_after'),
        ExtraFieldDefaultHelper(field_name='available'),
    ),
    m2m_instance_fields=('catalogs', 'conditions'),
)
