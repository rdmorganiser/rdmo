from rdmo.core.imports import (
    ElementImportHelper,
)

from .models import Option, OptionSet
from .serializers.v1 import OptionSerializer, OptionSetSerializer
from .validators import (
    OptionLockedValidator,
    OptionSetLockedValidator,
    OptionSetUniqueURIValidator,
    OptionUniqueURIValidator,
)

import_helper_option = ElementImportHelper(
    model = Option,
    model_path="options.option",
    validators=(OptionLockedValidator, OptionUniqueURIValidator),
    lang_fields=('text',),
    serializer = OptionSerializer,
    extra_fields = ('order', 'provider_key', 'additional_input'),
    m2m_instance_fields = ('conditions', ),
    m2m_through_instance_fields = [
        {'field_name': 'options', 'source_name': 'optionset',
         'target_name': 'option', 'through_name': 'optionset_options'}
    ]
)

import_helper_optionset = ElementImportHelper(
    model = OptionSet,
    model_path="options.optionset",
    validators=(OptionSetLockedValidator, OptionSetUniqueURIValidator),
    serializer = OptionSetSerializer,
    extra_fields=('additional_input',),
    reverse_m2m_through_instance_fields=[
        {'field_name': 'optionset', 'source_name': 'option',
         'target_name': 'optionset', 'through_name': 'option_optionsets'}
    ]
)
