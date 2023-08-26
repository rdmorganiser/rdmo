import logging

from django.contrib.sites.models import Site

from rdmo.core.imports import check_permissions, set_common_fields, set_lang_field, set_m2m_instances, validate_instance

from .models import View
from .validators import ViewLockedValidator, ViewUniqueURIValidator

logger = logging.getLogger(__name__)


def import_view(element, save=False, user=None):
    try:
        view = View.objects.get(uri=element.get('uri'))
    except View.DoesNotExist:
        view = View()

    set_common_fields(view, element)

    view.template = element.get('template')

    set_lang_field(view, 'title', element)
    set_lang_field(view, 'help', element)

    view.available = element.get('available', True)

    validate_instance(view, element, ViewLockedValidator, ViewUniqueURIValidator)

    check_permissions(view, element, user)

    if save and not element.get('errors'):
        if view.id:
            element['updated'] = True
            logger.info('View %s updated.', element.get('uri'))
        else:
            element['created'] = True
            logger.info('View created with uri %s.', element.get('uri'))

        view.save()
        set_m2m_instances(view, 'catalogs', element)
        view.sites.add(Site.objects.get_current())
        view.editors.add(Site.objects.get_current())

    return view
