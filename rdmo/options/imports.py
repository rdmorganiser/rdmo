import logging
from typing import Callable, Tuple

from django.contrib.sites.models import Site
from django.db import models

from rdmo.core.imports import (
    ElementImportHelper,
    check_permissions,
    set_m2m_instances,
    set_m2m_through_instances,
    set_reverse_m2m_through_instance,
    validate_instance,
)
from rdmo.options.validators import (
    OptionLockedValidator,
    OptionSetLockedValidator,
    OptionSetUniqueURIValidator,
    OptionUniqueURIValidator,
)

logger = logging.getLogger(__name__)


def import_option(
        instance: models.Model,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
        user: models.Model = None
    ):

    instance.order = element.get('order') or 0
    instance.provider_key = element.get('provider_key') or ''

    validate_instance(instance, element, *validators)

    check_permissions(instance, element, user)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_m2m_instances(instance, 'conditions', element)
        set_m2m_through_instances(instance, 'options', element, 'optionset', 'option', 'optionset_options')
        instance.editors.add(Site.objects.get_current())

    return instance


import_helper_option = ElementImportHelper(
    model="options.option",
    import_method=import_option,
    validators=(OptionLockedValidator, OptionUniqueURIValidator),
    lang_fields=('text',)
)


def import_optionset(
        instance: models.Model,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
        user: models.Model = None
    ):

    # lang_fields are already set in management/import.py

    instance.additional_input = element.get('additional_input') or ""

    validate_instance(instance, element, *validators)

    check_permissions(instance, element, user)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_reverse_m2m_through_instance(instance, 'optionset', element, 'option', 'optionset', 'option_optionsets')
        instance.editors.add(Site.objects.get_current())

    return instance


import_helper_optionset = ElementImportHelper(
    model="options.optionset",
    import_method=import_optionset,
    validators=(OptionSetLockedValidator, OptionSetUniqueURIValidator),
    lang_fields=None
)
