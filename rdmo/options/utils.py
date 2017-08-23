from rdmo.core.utils import get_ns_tag

from .models import OptionSet, Option


def import_options(optionsets_node):

    nsmap = optionsets_node.nsmap

    for optionset_node in optionsets_node.iterchildren():
        uri = optionset_node[get_ns_tag('dc:uri', nsmap)].text

        try:
            optionset = OptionSet.objects.get(uri=uri)
        except OptionSet.DoesNotExist:
            optionset = OptionSet()

        optionset.uri_prefix = uri.split('/options/')[0]
        optionset.key = uri.split('/')[-1]
        optionset.comment = optionset_node[get_ns_tag('dc:comment', nsmap)]
        optionset.order = optionset_node['order']
        optionset.save()

        for option_node in optionset_node.options.iterchildren():
            uri = option_node[get_ns_tag('dc:uri', nsmap)].text

            try:
                option = Option.objects.get(uri=uri)
            except Option.DoesNotExist:
                option = Option()

            option.optionset = optionset
            option.uri_prefix = uri.split('/options/')[0]
            option.key = uri.split('/')[-1]
            option.comment = option_node[get_ns_tag('dc:comment', nsmap)]
            option.order = option_node['order']
            for element in option_node['text']:
                setattr(option, 'text_' + element.get('lang'), element.text)
            option.additional_input = option_node['additional_input']
            option.save()
