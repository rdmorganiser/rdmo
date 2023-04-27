import logging

from rdmo.core.imports import (set_common_fields, set_lang_field,
                               set_m2m_instances, set_m2m_through_instances,
                               set_reverse_m2m_through_instance,
                               validate_instance)

from .models import Option, OptionSet
from .validators import (OptionLockedValidator, OptionSetLockedValidator,
                         OptionSetUniqueURIValidator, OptionUniqueURIValidator)

logger = logging.getLogger(__name__)


def import_optionset(element, save=False):
    try:
        optionset = OptionSet.objects.get(uri=element.get('uri'))
    except OptionSet.DoesNotExist:
        optionset = OptionSet()

    set_common_fields(optionset, element)

    optionset.order = element.get('order') or 0
    optionset.provider_key = element.get('provider_key') or ''

    if save and validate_instance(optionset, OptionSetLockedValidator, OptionSetUniqueURIValidator):
        if optionset.id:
            logger.info('OptionSet %s updated.', element.get('uri'))
        else:
            logger.info('OptionSet created with uri %s.', element.get('uri'))

        optionset.save()
        set_m2m_instances(optionset, 'conditions', element)
        set_m2m_through_instances(optionset, 'options', element, 'optionset', 'option', 'optionset_options')

        element['imported'] = True

    return optionset


def import_option(element, save=False):
    try:
        option = Option.objects.get(uri=element.get('uri'))
    except Option.DoesNotExist:
        option = Option()

    set_common_fields(option, element)

    option.additional_input = element.get('additional_input') or False

    set_lang_field(option, 'text', element)

    if save and validate_instance(option, OptionLockedValidator, OptionUniqueURIValidator):
        if option.id:
            logger.info('Option %s updated.', element.get('uri'))
        else:
            logger.info('Option created with uri %s.', element.get('uri'))

        option.save()
        set_reverse_m2m_through_instance(option, 'optionset', element, 'option', 'optionset', 'option_optionsets')

        element['imported'] = True

    return option
