import logging

from rdmo.core.imports import get_value_from_xml_node
from rdmo.core.utils import get_ns_map, get_ns_tag

log = logging.getLogger(__name__)


def import_conditions(optionsets_node):
    log.info("Importing options")

    nsmap = get_ns_map(optionsets_node.getroot())

    for optionset_node in optionsets_node.findall('conditions'):
        uri = optionset_node.find(get_ns_tag('dc:uri', nsmap)).text

        # try:
        #     optionset = OptionSet.objects.get(uri=uri)
        # except OptionSet.DoesNotExist:
        #     log.info(OptionSet.DoesNotExist)
        #     optionset = OptionSet()
        #
        # optionset.uri_prefix = uri.split('/options/')[0]
        # optionset.key = uri.split('/')[-1]
        # optionset.comment = get_value_from_xml_node(optionset_node, get_ns_tag('dc:comment', nsmap))
        # optionset.order = get_value_from_xml_node(optionset_node, 'order')
        # log.info('Saving optionset ' + str(optionset))
        # optionset.save()
        #
        # # for option_node in optionset_node.options.iterchildren():
        # for options_node in optionset_node.findall('options'):
        #     for option_node in options_node.findall('option'):
        #         uri = option_node.find(get_ns_tag('dc:uri', nsmap)).text
        #
        #         try:
        #             option = Option.objects.get(uri=uri)
        #         except Option.DoesNotExist:
        #             log.info(Option.DoesNotExist)
        #             option = Option()
        #
        #         option.optionset = optionset
        #         option.uri_prefix = uri.split('/options/')[0]
        #         option.key = uri.split('/')[-1]
        #         option.comment = get_value_from_xml_node(option_node, get_ns_tag('dc:comment', nsmap))
        #         log.info(get_value_from_xml_node(option_node, get_ns_tag('dc:comment', nsmap)))
        #         option.order = get_value_from_xml_node(option_node, 'order')
        #         for element in option_node.findall('text'):
        #             setattr(option, 'text_' + element.get('lang'), element.text)
        #         option.additional_input = utf8_to_bool(get_value_from_xml_node(option_node, 'additional_input'))
        #         log.info('Saving option ' + str(option))
        #         option.save()
