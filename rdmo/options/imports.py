import logging

from django.contrib.sites.models import Site

from rdmo.core.imports import (
    check_permissions,
    get_or_return_instance,
    make_import_info_msg,
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

    optionset, _created = get_or_return_instance(OptionSet, uri=element.get('uri'))
    element['created'] = _created
    element['updated'] = not _created

    _msg = make_import_info_msg(optionset._meta.verbose_name, _created, uri=element.get('uri'))

    set_common_fields(optionset, element)

    optionset.order = element.get('order') or 0
    optionset.provider_key = element.get('provider_key') or ''

    validate_instance(optionset, element, OptionSetLockedValidator, OptionSetUniqueURIValidator)

    check_permissions(optionset, element, user)

    if element.get('errors'):
        return optionset

    if save:
        logger.info(_msg)
        optionset.save()
        set_m2m_instances(optionset, 'conditions', element)
        set_m2m_through_instances(optionset, 'options', element, 'optionset', 'option', 'optionset_options')
        optionset.editors.add(Site.objects.get_current())

    return optionset


def import_option(element, save=False, user=None):

    option, _created = get_or_return_instance(Option, uri=element.get('uri'))
    element['created'] = _created
    element['updated'] = not _created

    _msg = make_import_info_msg(option._meta.verbose_name, _created, uri=element.get('uri'))


    set_common_fields(option, element)

    option.additional_input = element.get('additional_input') or ''

    set_lang_field(option, 'text', element)
    set_lang_field(option, 'help', element)
    set_lang_field(option, 'view_text', element)

    validate_instance(option, element, OptionLockedValidator, OptionUniqueURIValidator)

    check_permissions(option, element, user)

    if element.get('errors'):
        return option

    if save:
        logger.info(_msg)
        option.save()
        set_reverse_m2m_through_instance(option, 'optionset', element, 'option', 'optionset', 'option_optionsets')
        option.editors.add(Site.objects.get_current())

    return option
