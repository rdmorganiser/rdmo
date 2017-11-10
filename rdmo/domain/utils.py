from rdmo.core.utils import get_ns_tag
from rdmo.conditions.models import Condition
from rdmo.options.models import OptionSet

from .models import AttributeEntity, Attribute, Range, VerboseName


def import_domain(domain_node):

    nsmap = domain_node.nsmap

    for entity_node in domain_node.iterchildren():

        if entity_node.tag == 'entity':
            import_attribute_entity(entity_node, nsmap)
        else:
            import_attribute(entity_node, nsmap)


def import_attribute_entity(entity_node, nsmap, parent=None):

    uri = entity_node[get_ns_tag('dc:uri', nsmap)].text

    try:
        entity = AttributeEntity.objects.get(uri=uri, parent=parent)
    except AttributeEntity.DoesNotExist:
        entity = AttributeEntity()

    entity.parent = parent
    entity.uri_prefix = uri.split('/domain/')[0]
    entity.key = uri.split('/')[-1]
    entity.comment = entity_node[get_ns_tag('dc:comment', nsmap)]
    entity.is_collection = entity_node['is_collection'] == 'True'
    entity.save()

    if hasattr(entity_node, 'verbosename'):
        import_verbose_name(entity_node.verbosename, entity)

    if hasattr(entity_node, 'conditions'):
        for condition_node in entity_node.conditions.iterchildren():
            try:
                condition_uri = condition_node.get(get_ns_tag('dc:uri', nsmap))
                condition = Condition.objects.get(uri=condition_uri)
                entity.conditions.add(condition)
            except Condition.DoesNotExist:
                pass

    if hasattr(entity_node, 'children'):
        for child_node in entity_node.children.iterchildren():
            if child_node.tag == 'entity':
                import_attribute_entity(child_node, nsmap, parent=entity)
            else:
                import_attribute(child_node, nsmap, parent=entity)


def import_attribute(attribute_node, nsmap, parent=None):

    uri = attribute_node[get_ns_tag('dc:uri', nsmap)].text

    try:
        attribute = Attribute.objects.get(uri=uri)
    except Attribute.DoesNotExist:
        attribute = Attribute()

    attribute.parent = parent
    attribute.uri_prefix = uri.split('/domain/')[0]
    attribute.key = uri.split('/')[-1]
    attribute.comment = attribute_node[get_ns_tag('dc:comment', nsmap)]
    attribute.is_collection = attribute_node['is_collection'] == 'True'
    attribute.value_type = attribute_node['value_type']
    attribute.unit = attribute_node['unit']
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
    if verbosename_node is not None:
        try:
            try:
                verbosename = VerboseName.objects.get(attribute_entity=entity)
            except VerboseName.DoesNotExist:
                verbosename = VerboseName(attribute_entity=entity)

            for element in verbosename_node['name']:
                setattr(verbosename, 'name_' + element.get('lang'), element.text)
            for element in verbosename_node['name_plural']:
                setattr(verbosename, 'name_plural_' + element.get('lang'), element.text)
            verbosename.save()
        except AttributeError:
            pass


def import_range(range_node, attribute):
    if range_node is not None:
        try:
            try:
                range = Range.objects.get(attribute=attribute)
            except Range.DoesNotExist:
                range = Range(attribute=attribute)

            range.minimum = range_node['minimum']
            range.maximum = range_node['maximum']
            range.step = range_node['step']
            range.save()
        except AttributeError:
            pass
