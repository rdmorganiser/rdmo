import logging
from typing import Optional

from ..core.import_helpers import ElementImportHelper, ExtraFieldDefaultHelper
from .models import Attribute
from .validators import AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator

logger = logging.getLogger(__name__)


def get_default_path(instance: Optional[Attribute]=None):
    if instance is not None:
        return instance.build_path(instance.key, instance.parent)


import_helper_attribute = ElementImportHelper(
    model=Attribute,
    model_path="domain.attribute",
    common_fields=('uri_prefix', 'key', 'comment'),
    validators=(AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator),
    foreign_fields=('parent',),
    extra_fields=[ExtraFieldDefaultHelper(field_name='path', callback=get_default_path)],
)
