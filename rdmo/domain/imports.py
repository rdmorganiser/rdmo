import logging

from rdmo.core.imports import (
    ElementImportHelper,
)

from .models import Attribute
from .validators import AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator

logger = logging.getLogger(__name__)

import_helper_attribute = ElementImportHelper(
    model=Attribute,
    model_path="domain.attribute",
    common_fields=('uri_prefix', 'key', 'comment'),
    validators=(AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator),
    foreign_fields=('parent',),
    extra_fields=('path',),
)
