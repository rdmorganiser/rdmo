from rdmo.core.import_helpers import ElementImportHelper, ExtraFieldHelper, ThroughInstanceMapper

from .models import Option, OptionSet
from .validators import (
    OptionLockedValidator,
    OptionSetLockedValidator,
    OptionSetUniqueURIValidator,
    OptionUniqueURIValidator,
)

import_helper_optionset = ElementImportHelper(
    model=OptionSet,
    validators=(OptionSetLockedValidator, OptionSetUniqueURIValidator),
    extra_fields=(
        ExtraFieldHelper(field_name='order'),
        ExtraFieldHelper(field_name='provider_key', value=''),
    ),
    m2m_instance_fields=('conditions', ),
    m2m_through_instance_fields=[
        ThroughInstanceMapper(
            field_name='options',
            source_name='optionset',
            target_name='option',
            through_name='optionset_options'
        ),
    ]
)


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

    option.additional_input = element.get('additional_input') or ''

    set_lang_field(option, 'text', element)
    set_lang_field(option, 'help', element)
    set_lang_field(option, 'default_text', element)
    set_lang_field(option, 'view_text', element)

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
