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

import_helper_option = ElementImportHelper(
    model=Option,
    validators=(OptionLockedValidator, OptionUniqueURIValidator),
    lang_fields=('text', 'help', 'view_text'),
    extra_fields=(
        ExtraFieldHelper(field_name='additional_input', value=Option.ADDITIONAL_INPUT_NONE),
        ),
    reverse_m2m_through_instance_fields=[
        ThroughInstanceMapper(
            field_name='optionset',
            source_name='option',
            target_name='optionset',
            through_name='option_optionsets'
        ),
    ]
)
