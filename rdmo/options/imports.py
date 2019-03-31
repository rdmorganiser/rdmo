import logging

from django.core.exceptions import ValidationError

from rdmo.core.imports import set_lang_field
from rdmo.core.xml import flat_xml_to_elements, filter_elements_by_type
from rdmo.core.utils import get_languages

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

    optionset.uri_prefix = element['uri_prefix'] or ''
    optionset.key = element['key'] or ''
    optionset.comment = element['comment'] or ''

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

    option.uri_prefix = element['uri_prefix'] or ''
    option.key = element['key'] or ''
    option.comment = element['comment'] or ''

    option.order = element['order']
    option.additional_input = element['additional_input']

    for lang_code, lang_string, lang_field in get_languages():
        set_lang_field(option, 'text', element, lang_code, lang_field)

    try:
        OptionUniquePathValidator(option).validate()
    except ValidationError as e:
        log.info('Option not saving "%s" due to validation error (%s).', element['uri'], e)
        pass
    else:
        log.info('Option saving to "%s".', element['uri'])
        option.save()
