import logging
from typing import Callable, Tuple

from rdmo.core.imports import (
    ElementImportHelper,
    set_m2m_instances,
    set_m2m_through_instances,
    set_reverse_m2m_through_instance,
    validate_instance,
)

from .models import Option, OptionSet
from .serializers.v1 import OptionSerializer, OptionSetSerializer
from .validators import (
    OptionLockedValidator,
    OptionSetLockedValidator,
    OptionSetUniqueURIValidator,
    OptionUniqueURIValidator,
)

logger = logging.getLogger(__name__)


def import_option(
        instance: Option,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
    ):
    # check_permissions already done in management/import.py
    # extra_fields are set in in management/import.py
    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_m2m_instances(instance, 'conditions', element)
        set_m2m_through_instances(instance, 'options', element, 'optionset', 'option', 'optionset_options')
        # sites and editors are added in management/import.py

    return instance


import_helper_option = ElementImportHelper(
    model="options.option",
    import_func=import_option,
    validators=(OptionLockedValidator, OptionUniqueURIValidator),
    lang_fields=('text',),
    serializer = OptionSerializer,
    extra_fields = ('order', 'provider_key', 'additional_input')
)


def import_optionset(
        instance: OptionSet,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
    ):
    # lang_fields are already set in management/import.py
    # check_permissions already done in management/import.py
    # extra_fields are set in in management/import.py
    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_reverse_m2m_through_instance(instance, 'optionset', element, 'option', 'optionset', 'option_optionsets')
        # sites and editors are added in management/import.py

    return instance


import_helper_optionset = ElementImportHelper(
    model="options.optionset",
    import_func=import_optionset,
    validators=(OptionSetLockedValidator, OptionSetUniqueURIValidator),
    serializer = OptionSetSerializer,
    extra_fields=('additional_input',)
)
