from rdmo.core.import_helpers import ElementImportHelper, ExtraFieldHelper

from .models import Task
from .validators import TaskLockedValidator, TaskUniqueURIValidator

import_helper_task = ElementImportHelper(
    model=Task,
    validators=(TaskLockedValidator, TaskUniqueURIValidator),
    lang_fields=('title', 'text'),
    foreign_fields=('start_attribute', 'end_attribute'),
    extra_fields=(
        ExtraFieldHelper(field_name='order'),
        ExtraFieldHelper(field_name='days_before'),
        ExtraFieldHelper(field_name='days_after'),
        ExtraFieldHelper(field_name='available', overwrite_in_element=True),
    ),
    m2m_instance_fields=('catalogs', 'conditions'),
)
