import logging

from django.contrib.sites.models import Site

from rdmo.core.imports import (
    check_permissions,
    set_common_fields,
    set_lang_field,
    set_m2m_instances,
    set_m2m_through_instances,
    set_reverse_m2m_through_instance,
    validate_instance,
)

from .models import Option, OptionSet
from .validators import (
    OptionLockedValidator,
    OptionSetLockedValidator,
    OptionSetUniqueURIValidator,
    OptionUniqueURIValidator,
)

logger = logging.getLogger(__name__)


def import_optionset(element, save=False, user=None):
    try:
        optionset = OptionSet.objects.get(uri=element.get('uri'))
    except OptionSet.DoesNotExist:
        optionset = OptionSet()

    set_common_fields(optionset, element)

    optionset.order = element.get('order') or 0
    optionset.provider_key = element.get('provider_key') or ''

    validate_instance(optionset, element, OptionSetLockedValidator, OptionSetUniqueURIValidator)

    check_permissions(optionset, element, user)

    if save and not element.get('errors'):
        if optionset.id:
            element['updated'] = True
            logger.info('OptionSet %s updated.', element.get('uri'))
        else:
            element['created'] = True
            logger.info('OptionSet created with uri %s.', element.get('uri'))

        optionset.save()
        set_m2m_instances(optionset, 'conditions', element)
        set_m2m_through_instances(optionset, 'options', element, 'optionset', 'option', 'optionset_options')
        optionset.editors.add(Site.objects.get_current())

    return optionset


def import_option(element, save=False, user=None):
    try:
        option = Option.objects.get(uri=element.get('uri'))
    except Option.DoesNotExist:
        option = Option()

    set_common_fields(option, element)

    option.additional_input = element.get('additional_input') or False

    set_lang_field(option, 'text', element)

    validate_instance(option, element, OptionLockedValidator, OptionUniqueURIValidator)

    check_permissions(option, element, user)

    if save and not element.get('errors'):
        if option.id:
            element['updated'] = True
            logger.info('Option %s updated.', element.get('uri'))
        else:
            element['created'] = True
            logger.info('Option created with uri %s.', element.get('uri'))

        option.save()
        set_reverse_m2m_through_instance(option, 'optionset', element, 'option', 'optionset', 'option_optionsets')
        option.editors.add(Site.objects.get_current())

    return option
