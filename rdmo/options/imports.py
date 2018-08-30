import logging

from django.core.exceptions import ValidationError

from rdmo.core.xml import flat_xml_to_elements, filter_elements_by_type

from .models import Option, OptionSet
from .validators import OptionSetUniqueKeyValidator, OptionUniquePathValidator

log = logging.getLogger(__name__)


def import_options(root):
    elements = flat_xml_to_elements(root)

    for element in filter_elements_by_type(elements, 'optionset'):
        import_optionset(element)

    for element in filter_elements_by_type(elements, 'option'):
        import_option(element)


def import_optionset(element):
    try:
        optionset = OptionSet.objects.get(uri=element['uri'])
    except OptionSet.DoesNotExist:
        log.info('OptionSet not in db. Created with uri %s.', element['uri'])
        optionset = OptionSet()

    optionset.uri_prefix = element['uri_prefix']
    optionset.key = element['key']
    optionset.comment = element['comment']

    optionset.order = element['order']

    try:
        OptionSetUniqueKeyValidator(optionset).validate()
    except ValidationError as e:
        log.info('OptionSet not saving "%s" due to validation error (%s).', element['uri'], e)
        return
    else:
        log.info('OptionSet saving to "%s".', element['uri'])
        optionset.save()


def import_option(element):
    try:
        option = Option.objects.get(uri=element['uri'])
    except Option.DoesNotExist:
        log.info('Option not in db. Created with uri %s.', element['uri'])
        option = Option()

    try:
        option.optionset = OptionSet.objects.get(uri=element['optionset'])
    except OptionSet.DoesNotExist:
        log.info('OptionSet not in db. Skipping.')
        return

    option.uri_prefix = element['uri_prefix']
    option.key = element['key']
    option.comment = element['comment']

    option.order = element['order']

    option.text_en = element['text_en']
    option.text_de = element['text_de']

    option.additional_input = element['additional_input']

    try:
        OptionUniquePathValidator(option).validate()
    except ValidationError as e:
        log.info('Option not saving "%s" due to validation error (%s).', element['uri'], e)
        pass
    else:
        log.info('Option saving to "%s".', element['uri'])
        option.save()
