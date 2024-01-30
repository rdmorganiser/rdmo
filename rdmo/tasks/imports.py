from rdmo.core.imports import ElementImportHelper

from .serializers.v1 import TaskSerializer
from .validators import TaskLockedValidator, TaskUniqueURIValidator

import_helper_task = ElementImportHelper(
    model="tasks.task",
    validators=(TaskLockedValidator, TaskUniqueURIValidator),
    lang_fields=('title', 'text'),
    foreign_fields=('start_attribute', 'end_attribute'),
    serializer=TaskSerializer,
    extra_fields=('order', 'days_before', 'days_after', 'available'),
    m2m_instance_fields=('catalogs', 'conditions'),
)
