import logging

from django.core.exceptions import ValidationError

from rdmo.core.xml import flat_xml_to_dictlist, get_ns_map, get_ns_tag, get_uri

from .models import Attribute
from .validators import AttributeUniquePathValidator

log = logging.getLogger(__name__)


def import_domain(root):
    log.info('Starting to parse domain node')
    domains = flat_xml_to_dictlist(root)

    print(domains)

#     for el in root.findall('attribute'):
#         uri = get_uri(el, nsmap)
#         parent = get_element_attrib(el, 'parent')
#
#         try:
#             attribute = Attribute.objects.get(uri=uri, parent=parent)
#         except Attribute.DoesNotExist:
#             attribute = Attribute()
#             log.info('Attribute not in db. Created with uri ' + str(uri))
#
#         attribute.uri = uri
#         attribute.comment = get_element_text(el, 'dc:comment', nsmap)
#         # attribute.parent = get_uri(el.find('parent'), nsmap)
#         # log.info("---> " + str(attribute.parent))
#
#         from django.forms.models import model_to_dict
#         log.info(model_to_dict(attribute))
#
#         # try:
#         #     AttributeUniquePathValidator(attribute).validate()
#         # except ValidationError:
#         #     log.info('Attribute not saving "' + str(uri) + '" due to validation error')
#         #     pass
#         # else:
#         #     log.info('Attribute saving to "' + str(uri) + '", parent "' + str(parent) + '"')
#             # attribute.save()
#
# #     nsmap = get_ns_map(domain_node.getroot())
# #
# #     for attribute_node in domain_node.findall('attribute'):
# #         import_attribute(attribute_node, nsmap)
# #
# #
# # def import_attribute(attribute_node, nsmap, parent=None):
# #     uri = get_uri(attribute_node, nsmap)
# #
# #     try:
# #         attribute = Attribute.objects.get(uri=uri, parent=parent)
# #     except Attribute.DoesNotExist:
# #         attribute = Attribute()
# #         log.info('Attribute not in db. Created with uri ' + str(uri))
# #     else:
# #         log.info('Attribute does exist. Loaded from uri ' + str(uri))
# #
# #     attribute.parent = parent
# #     attribute.uri_prefix = uri.split('/domain/')[0]
# #     attribute.key = uri.split('/')[-1]
# #     attribute.comment = get_value_from_treenode(attribute_node, get_ns_tag('dc:comment', nsmap))
# #
# #     try:
# #         AttributeUniquePathValidator(attribute).validate()
# #     except ValidationError:
# #         log.info('Attribute not saving "' + str(uri) + '" due to validation error')
# #         pass
# #     else:
# #         log.info('Attribute saving to "' + str(uri) + '", parent "' + str(parent) + '"')
# #         attribute.save()
# #
# #     for child_node in attribute_node.find('children').findall('attribute'):
# #         import_attribute(child_node, nsmap, parent=attribute)
