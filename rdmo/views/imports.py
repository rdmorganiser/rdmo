import logging

from django.contrib.sites.models import Site

from rdmo.core.imports import (set_m2m_instances, set_common_fields,
                               set_lang_field, validate_instance)

from .models import View
from .validators import ViewLockedValidator, ViewUniqueURIValidator

logger = logging.getLogger(__name__)


def import_view(element, save=False):
    try:
        view = View.objects.get(uri=element.get('uri'))
    except View.DoesNotExist:
        view = View()

    set_common_fields(view, element)

    view.template = element.get('template')

    set_lang_field(view, 'title', element)
    set_lang_field(view, 'help', element)

    if save and validate_instance(view, ViewLockedValidator, ViewUniqueURIValidator):
        if view.id:
            logger.info('View created with uri %s.', element.get('uri'))
        else:
            logger.info('View %s updated.', element.get('uri'))

        view.save()
        view.sites.add(Site.objects.get_current())
        set_m2m_instances(view, 'catalogs', element)
        view.imported = True

    return view
