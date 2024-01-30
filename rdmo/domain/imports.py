import logging

from rdmo.core.imports import (
    ElementImportHelper,
)

from .serializers.v1 import BaseAttributeSerializer
from .validators import AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator

logger = logging.getLogger(__name__)

import_helper_attribute = ElementImportHelper(
    model="domain.attribute",
    validators=(AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator),
    foreign_fields=('parent',),
    extra_fields=('path',),
    serializer=BaseAttributeSerializer,
)
