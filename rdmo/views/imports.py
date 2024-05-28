from rdmo.core.import_helpers import ElementImportHelper, ExtraFieldDefaultHelper

from .models import View
from .validators import ViewLockedValidator, ViewUniqueURIValidator

import_helper_view = ElementImportHelper(
    model=View,
    model_path="views.view",
    validators=(ViewLockedValidator, ViewUniqueURIValidator),
    lang_fields=('help', 'title'),
    extra_fields=(
        ExtraFieldDefaultHelper(field_name='order'),
        ExtraFieldDefaultHelper(field_name='template'),
        ExtraFieldDefaultHelper(field_name='available'),
    ),
    m2m_instance_fields=('catalogs',),
)
