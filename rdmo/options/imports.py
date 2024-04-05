from ..core.import_helpers import ElementImportHelper, ExtraFieldDefaultHelper, ThroughInstanceMapper
from .models import Option, OptionSet
from .validators import (
    OptionLockedValidator,
    OptionSetLockedValidator,
    OptionSetUniqueURIValidator,
    OptionUniqueURIValidator,
)

import_helper_optionset = ElementImportHelper(
    model = OptionSet,
    model_path = "options.optionset",
    validators = (OptionSetLockedValidator, OptionSetUniqueURIValidator),
    extra_fields = (
        ExtraFieldDefaultHelper(field_name='order'),
        ExtraFieldDefaultHelper(field_name='provider_key', value=''),
    ),
    m2m_instance_fields = ('conditions', ),
    m2m_through_instance_fields = [
        ThroughInstanceMapper(
            field_name='options',
            source_name='optionset',
            target_name='option',
            through_name='optionset_options'
        ),
    ]
)

import_helper_option = ElementImportHelper(
    model = Option,
    model_path = "options.option",
    validators = (OptionLockedValidator, OptionUniqueURIValidator),
    lang_fields = ('text', 'help', 'view_text'),
    extra_fields = (
        ExtraFieldDefaultHelper(field_name='additional_input'),
        ),
    reverse_m2m_through_instance_fields = [
        ThroughInstanceMapper(
            field_name='optionset',
            source_name='option',
            target_name='optionset',
            through_name='option_optionsets'
        ),
    ]
)
