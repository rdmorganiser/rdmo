import logging

from django.core.exceptions import ValidationError

from rdmo.core.imports import get_value_from_treenode, make_bool
from rdmo.core.utils import get_ns_map, get_ns_tag, get_uri

from .models import AttributeEntity, Attribute
from .validators import AttributeEntityUniquePathValidator

log = logging.getLogger(__name__)


def import_domain(domain_node):
    log.info('Starting to parse domain node')
    nsmap = get_ns_map(domain_node.getroot())

    for entity_node in domain_node.findall('entity'):
        import_attribute_entity(entity_node, nsmap)
    for entity_node in domain_node.findall('attribute'):
        import_attribute(entity_node, nsmap)


def import_attribute_entity(entity_node, nsmap, parent=None):
    uri = get_uri(entity_node, nsmap)

    try:
        entity = AttributeEntity.objects.get(uri=uri, parent=parent)
    except AttributeEntity.DoesNotExist:
        entity = AttributeEntity()
        log.info('Entity not in db. Created with uri ' + str(uri))
    else:
        log.info('Entity does exist. Loaded from uri ' + str(uri))

    entity.parent = parent
    entity.uri_prefix = uri.split('/domain/')[0]
    entity.key = uri.split('/')[-1]
    entity.comment = get_value_from_treenode(entity_node, get_ns_tag('dc:comment', nsmap))

    try:
        AttributeEntityUniquePathValidator(entity).validate()
    except ValidationError:
        log.info('Entity not saving "' + str(uri) + '" due to validation error')
        pass
    else:
        log.info('Entity saving to "' + str(uri) + '", parent "' + str(parent) + '"')
        entity.save()

    for child_node in entity_node.find('children').findall('entity'):
        import_attribute_entity(child_node, nsmap, parent=entity)
    for child_node in entity_node.find('children').findall('attribute'):
        import_attribute(child_node, nsmap, parent=entity)


def import_attribute(attribute_node, nsmap, parent=None):
    attribute_uri = get_uri(attribute_node, nsmap)

    try:
        attribute = Attribute.objects.get(uri=attribute_uri)
    except Attribute.DoesNotExist:
        log.info('Attribute not in db. Created with uri ' + str(attribute_uri))
        attribute = Attribute()
        pass
    else:
        log.info('Attribute does exist. Loaded from uri ' + str(attribute_uri))

    attribute.uri = attribute_uri
    attribute.parent = parent
    attribute.uri_prefix = attribute_uri.split('/domain/')[0]

    attribute.key = attribute_uri.split('/')[-1]
    attribute.comment = get_value_from_treenode(attribute_node, get_ns_tag('dc:comment', nsmap))

    try:
        AttributeEntityUniquePathValidator(attribute).validate()
    except ValidationError:
        log.info('Attribute not saving "' + str(attribute_uri) + '" due to validation error')
        pass
    else:
        log.info('Attribute saving to "' + str(attribute_uri) + '", parent "' + str(parent) + '"')
        attribute.save()
