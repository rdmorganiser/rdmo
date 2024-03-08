from rdmo.core.imports import ElementImportHelper

from .models import Task
from .validators import TaskLockedValidator, TaskUniqueURIValidator

import_helper_task = ElementImportHelper(
    model=Task,
    model_path="tasks.task",
    validators=(TaskLockedValidator, TaskUniqueURIValidator),
    lang_fields=('title', 'text'),
    foreign_fields=('start_attribute', 'end_attribute'),
    extra_fields=('order', 'days_before', 'days_after', 'available'),
    m2m_instance_fields=('catalogs', 'conditions'),
)
