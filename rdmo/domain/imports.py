import logging

from django.core.exceptions import ValidationError

from rdmo.core.xml import flat_xml_to_dictlist

from .models import Attribute
from .validators import AttributeUniquePathValidator

log = logging.getLogger(__name__)


def import_domain(root):
    log.info('Starting to parse domain node')
    dictlist = flat_xml_to_dictlist(root)

    for entry in dictlist:
        # TODO: implement method to fetch the parent
        parent = None
        try:
            attribute = Attribute.objects.get(uri=entry['uri'], parent=parent)
        except Attribute.DoesNotExist:
            attribute = Attribute()
            log.info('Attribute not in db. Created with uri ' + str(entry['uri']))

        attribute.parent = parent
        attribute.uri = entry['uri']
        attribute.uri_prefix = entry['uri_prefix']
        attribute.key = entry['key']
        attribute.comment = entry['comment']
        attribute.path = entry['path']

        try:
            AttributeUniquePathValidator(attribute).validate()
        except ValidationError:
            log.info('Attribute not saving "' + str(entry['uri']) + '" due to validation error')
            pass
        else:
            log.info('Attribute saving to "' + str(entry['uri']) + '", parent "' + str(entry['parent']) + '"')
            # attribute.save()
