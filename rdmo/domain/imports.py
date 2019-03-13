import logging

from django.core.exceptions import ValidationError

from rdmo.core.xml import flat_xml_to_elements, filter_elements_by_type

from .models import Attribute
from .validators import AttributeUniquePathValidator

log = logging.getLogger(__name__)


def import_domain(root):
    elements = flat_xml_to_elements(root)

    for element in filter_elements_by_type(elements, 'attribute'):
        import_attribute(element)


def import_attribute(element):
    try:
        attribute = Attribute.objects.get(uri=element['uri'])
    except Attribute.DoesNotExist:
        log.info('Attribute not in db. Created with uri %s.', element['uri'])
        attribute = Attribute()

    attribute.parent = None
    if element['parent']:
        try:
            attribute.parent = Attribute.objects.get(uri=element['parent'])
        except Attribute.DoesNotExist:
            log.info('Parent not in db. Created with uri %s.', element['uri'])

    attribute.uri_prefix = element['uri_prefix'] or ''
    attribute.key = element['key'] or ''
    attribute.comment = element['comment'] or ''

    try:
        AttributeUniquePathValidator(attribute).validate()
    except ValidationError as e:
        log.info('Attribute not saving "%s" due to validation error (%s).', element['uri'], e)
        pass
    else:
        log.info('Attribute saving to "%s", parent "%s".', element['uri'], element['parent'])
        attribute.save()
