import logging

from django.core.exceptions import ValidationError

from rdmo.core.imports import get_value_from_treenode, make_bool
from rdmo.core.utils import get_ns_map, get_ns_tag, get_uri
from rdmo.conditions.models import Condition
from rdmo.options.models import OptionSet

from .models import AttributeEntity, Attribute, VerboseName
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
    entity.is_collection = make_bool(entity_node.find('is_collection').text)
    try:
        AttributeEntityUniquePathValidator(entity).validate()
    except ValidationError:
        log.info('Entity not saving "' + str(uri) + '" due to validation error')
        pass
    else:
        log.info('Entity saving to "' + str(uri) + '", parent "' + str(parent) + '"')
        entity.save()

    if entity_node.find('verbosename').text is not None:
        import_verbose_name(get_value_from_treenode(entity_node, 'verbosename'), entity)

    if entity_node.find('conditions') is not None:
        for condition_node in entity_node.find('conditions').findall('condition'):
            try:
                condition_uri = get_uri(condition_node, nsmap, 'plain')
                condition = Condition.objects.get(uri=condition_uri)
                entity.conditions.add(condition)
            except Condition.DoesNotExist:
                log.info('Condition import failed: ' + str(Condition.DoesNotExist))
                pass

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
    attribute.is_collection = make_bool(attribute_node.find('is_collection').text)
    attribute.value_type = get_value_from_treenode(attribute_node, 'value_type')
    attribute.unit = get_value_from_treenode(attribute_node, 'unit')
    try:
        AttributeEntityUniquePathValidator(attribute).validate()
    except ValidationError:
        log.info('Attribute not saving "' + str(attribute_uri) + '" due to validation error')
        pass
    else:
        log.info('Attribute saving to "' + str(attribute_uri) + '", parent "' + str(parent) + '"')
        attribute.save()

    if hasattr(attribute_node, 'range'):
        import_verbose_name(attribute_node.range, attribute)

    if hasattr(attribute_node, 'verbosename'):
        import_verbose_name(attribute_node.verbosename, attribute)

    if hasattr(attribute_node, 'optionsets'):
        for optionset_node in attribute_node.optionsets.iterchildren():
            try:
                optionset_uri = optionset_node.get(get_ns_tag('dc:uri', nsmap))
                optionset = OptionSet.objects.get(uri=optionset_uri)
                attribute.optionsets.add(optionset)
            except OptionSet.DoesNotExist:
                pass

    if hasattr(attribute_node, 'conditions'):
        for condition_node in attribute_node.conditions.iterchildren():
            try:
                condition_uri = condition_node.get(get_ns_tag('dc:uri', nsmap))
                condition = Condition.objects.get(uri=condition_uri)
                attribute.conditions.add(condition)
            except Condition.DoesNotExist:
                pass


def import_verbose_name(verbosename_node, entity):
    try:
        try:
            verbosename = VerboseName.objects.get(attribute_entity=entity)
        except VerboseName.DoesNotExist:
            verbosename = VerboseName(attribute_entity=entity)
        for element in verbosename_node.findall('name'):
            setattr(verbosename, 'name_' + element.get('lang'), element.text)
        for element in verbosename_node.findall('name_plural'):
            setattr(verbosename, 'name_plural_' + element.get('lang'), element.text)
        log.info('Verbosename saving ' + str(verbosename))
        verbosename.save()
    except Exception as e:
        log.info('Verbosename, an exception occured: ' + str(e))
        pass
