import logging
from typing import Callable, Tuple

from django.contrib.sites.models import Site

from rdmo.core.imports import (
    ElementImportHelper,
    set_m2m_instances,
    validate_instance,
)
from rdmo.views.validators import ViewLockedValidator, ViewUniqueURIValidator

from .models import View

logger = logging.getLogger(__name__)


def import_view(
        instance: View,
        element: dict,
        validators: Tuple[Callable],
        save: bool = False,
    ):
    # check_permissions already done in management/import.py

    instance.order = element.get('order') or 0
    instance.template = element.get('template')

    instance.available = element.get('available', True)

    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return instance

    if save:
        instance.save()
        set_m2m_instances(instance, 'catalogs', element)
        instance.sites.add(Site.objects.get_current())
        instance.editors.add(Site.objects.get_current())

    return instance


import_helper_view = ElementImportHelper(
    model="views.view",
    import_func=import_view,
    validators=(ViewLockedValidator, ViewUniqueURIValidator),
    lang_fields=( 'help', 'title')
)
