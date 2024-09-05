import logging
from typing import Optional

from rdmo.core.import_helpers import ElementImportHelper, ExtraFieldHelper

from .models import Attribute
from .validators import AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator

logger = logging.getLogger(__name__)


def build_attribute_path(instance: Optional[Attribute]=None):
    if instance is not None:
        return instance.build_path(instance.key, instance.parent)

def build_attribute_uri(instance: Optional[Attribute]=None):
    if instance is not None:
        return instance.build_uri(instance.uri_prefix, instance.path)


import_helper_attribute = ElementImportHelper(
    model=Attribute,
    common_fields=('uri_prefix', 'key', 'comment'),
    validators=(AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator),
    foreign_fields=('parent',),
    extra_fields=(
        ExtraFieldHelper(field_name='path', callback=build_attribute_path, overwrite_in_element=True),
        ExtraFieldHelper(field_name='uri', callback=build_attribute_uri, overwrite_in_element=True),
    )
)
