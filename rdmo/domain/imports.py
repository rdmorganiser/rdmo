import logging

from django.core.exceptions import ValidationError

from rdmo.core.xml import flat_xml_to_dictlist

from .models import Attribute
from .validators import AttributeUniquePathValidator

log = logging.getLogger(__name__)


def import_domain(root):
    log.info('Parsing domain node')
    elements = flat_xml_to_dictlist(root)

    for element in elements:
        try:
            attribute = Attribute.objects.get(uri=element['uri'])
        except Attribute.DoesNotExist:
            log.info('Attribute not in db. Created with uri %s.', element['uri'])
            attribute = Attribute()

        if element['parent']:
            try:
                attribute.parent = Attribute.objects.get(uri=element['parent'])
            except Attribute.DoesNotExist:
                log.info('Parent not in db. Created with uri %s.', element['uri'])
                attribute.parent = None
        else:
            attribute.parent = None

        attribute.uri_prefix = element['uri_prefix']
        attribute.key = element['key']
        attribute.comment = element['comment']

        try:
            AttributeUniquePathValidator(attribute).validate()
        except ValidationError as e:
            log.info('Attribute not saving "%s" due to validation error (%s).', element['uri'], e)
            pass
        else:
            log.info('Attribute saving to "%s", parent "%s".', element['uri'], element['parent'])
            attribute.save()
