import logging
from typing import Callable, Tuple

from django.contrib.sites.models import Site
from django.db import models

from rdmo.core.imports import (
    check_permissions,
    set_lang_field,
    set_m2m_instances,
    set_m2m_through_instances,
    set_reverse_m2m_through_instance,
    validate_instance,
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


def import_optionset(
        instance: models.Model,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
        user: models.Model = None
    ):

    instance.additional_input = element.get('additional_input') or ""

    set_lang_field(instance, 'text', element)
    set_lang_field(instance, 'help', element)
    set_lang_field(instance, 'view_text', element)

    validate_instance(instance, element, *validators)

    check_permissions(instance, element, user)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_reverse_m2m_through_instance(instance, 'optionset', element, 'option', 'optionset', 'option_optionsets')
        instance.editors.add(Site.objects.get_current())

    return instance
