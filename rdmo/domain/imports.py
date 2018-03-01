import logging

from rdmo.core.imports import get_value_from_xml_node
from rdmo.core.utils import get_ns_map, get_ns_tag
from rdmo.conditions.models import Condition
from rdmo.options.models import OptionSet

from .models import AttributeEntity, Attribute, VerboseName

log = logging.getLogger(__name__)


def import_domain(domain_node):
    nsmap = get_ns_map(domain_node.getroot())
    log.info('Starting to parse domain node')
    for entity_node in domain_node.iter():
        if entity_node.tag == 'entity':
            import_attribute_entity(entity_node, nsmap)
        elif entity_node.tag == 'attribute':
            import_attribute(entity_node, nsmap)


def import_attribute_entity(entity_node, nsmap, parent=None):
    uri = entity_node.find(get_ns_tag('dc:uri', nsmap)).text
    log.info('Importing attribute_entity with uri "' + uri + '"...')

    try:
        entity = AttributeEntity.objects.get(uri=uri, parent=parent)
    except AttributeEntity.DoesNotExist:
        log.info('Attribute entity import: ' + str(AttributeEntity.DoesNotExist))
        entity = AttributeEntity()

    entity.parent = parent
    entity.uri_prefix = uri.split('/domain/')[0]
    entity.key = uri.split('/')[-1]
    entity.comment = get_value_from_xml_node(entity_node, get_ns_tag('dc:comment', nsmap))
    entity.is_collection = entity_node.find('is_collection') == 'True'
    log.info('Saving entity ' + str(entity))
    entity.save()

    if entity_node.find('verbosename').text is not None:
        import_verbose_name(get_value_from_xml_node(entity_node, 'verbosename'), entity)

    if entity_node.find('conditions') is not None:
        for condition_node in entity_node.find('conditions').findall('condition'):
            try:
                condition_uri = condition_node.get(get_ns_tag('dc:uri', nsmap))
                condition = Condition.objects.get(uri=condition_uri)
                entity.conditions.add(condition)
            except Condition.DoesNotExist:
                log.info('Condition import failed: ' + str(Condition.DoesNotExist))
                pass

    for child_node in entity_node.findall('children'):
        if child_node.tag == 'entity':
            import_attribute_entity(child_node, nsmap, parent=entity)
        else:
            import_attribute(child_node, nsmap, parent=entity)


def import_attribute(attribute_node, nsmap, parent=None):
    try:
        uri = attribute_node.find(get_ns_tag('dc:uri', nsmap)).text
    except Exception as e:
        log.error(e)
    else:
        log.info('Importing attribute with uri "' + uri + '"...')

        try:
            attribute = Attribute.objects.get(uri=uri)
        except Attribute.DoesNotExist:
            attribute = Attribute()

        attribute.parent = parent
        attribute.uri_prefix = uri.split('/domain/')[0]
        attribute.key = uri.split('/')[-1]
        attribute.comment = get_value_from_xml_node(attribute_node, get_ns_tag('dc:comment', nsmap))
        attribute.is_collection = attribute_node.find('is_collection') == 'True'
        attribute.value_type = get_value_from_xml_node(attribute_node, 'value_type')
        attribute.unit = get_value_from_xml_node(attribute_node, 'unit')
        log.info('Saving attribute ' + str(attribute))
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
        log.info('Saving verbosename ' + str(verbosename))
        verbosename.save()
    except Exception as e:
        log.info('An exception occured: ' + str(e))
        pass
