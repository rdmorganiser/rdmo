import logging

from rdmo.conditions.models import Condition
from rdmo.core.imports import (get_instance, get_m2m_instances,
                               set_common_fields, set_foreign_field,
                               set_lang_field, set_temporary_fields,
                               validate_instance)

from .models import Option, OptionSet
from .validators import OptionSetUniqueKeyValidator, OptionUniquePathValidator

logger = logging.getLogger(__name__)


def import_optionset(element, save=[]):
    optionset = get_instance(element, OptionSet)

    set_common_fields(optionset, element)
    set_temporary_fields(optionset, element)

    optionset.order = element.get('order')

    conditions = get_m2m_instances(optionset, 'conditions', element, Condition)

    validate_instance(optionset, OptionSetUniqueKeyValidator)

    if optionset.uri in save:
        if optionset.id:
            logger.info('OptionSet created with uri %s.', element.get('uri'))
        else:
            logger.info('OptionSet %s updated.', element.get('uri'))

        optionset.save()
        optionset.conditions.set(conditions)

    return optionset


def import_option(element, save=[]):
    option = get_instance(element, Option)

    set_common_fields(option, element)
    set_temporary_fields(option, element)

    set_foreign_field(option, 'optionset', element, OptionSet)

    option.order = element.get('order')
    option.additional_input = element.get('additional_input')

    set_lang_field(option, 'text', element)

    validate_instance(option, OptionUniquePathValidator)

    if option.uri in save:
        if option.id:
            logger.info('Option created with uri %s.', element.get('uri'))
        else:
            logger.info('Option %s updated.', element.get('uri'))

        option.save()

    return option
