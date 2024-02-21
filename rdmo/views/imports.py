from rdmo.core.imports import ElementImportHelper

from .models import View
from .serializers.v1 import ViewSerializer
from .validators import ViewLockedValidator, ViewUniqueURIValidator

import_helper_view = ElementImportHelper(
    model=View,
    model_path="views.view",
    validators=(ViewLockedValidator, ViewUniqueURIValidator),
    lang_fields=('help', 'title'),
    serializer=ViewSerializer,
    extra_fields=('order', 'template', 'available'),
    m2m_instance_fields=('catalogs',),
)
