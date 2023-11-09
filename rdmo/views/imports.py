import logging

from django.contrib.sites.models import Site

from rdmo.core.imports import (
    check_permissions,
    get_or_return_instance,
    make_import_info_msg,
    set_common_fields,
    set_lang_field,
    set_m2m_instances,
    validate_instance,
)

from .models import View
from .validators import ViewLockedValidator, ViewUniqueURIValidator

logger = logging.getLogger(__name__)


def import_view(element, save=False, user=None):

    view, _created = get_or_return_instance(View, uri=element.get('uri'))
    element['created'] = _created
    element['updated'] = not _created

    _msg = make_import_info_msg(view._meta.verbose_name, _created, uri=element.get('uri'))

    set_common_fields(view, element)

    view.order = element.get('order') or 0
    view.template = element.get('template')

    set_lang_field(view, 'title', element)
    set_lang_field(view, 'help', element)

    view.available = element.get('available', True)

    validate_instance(view, element, ViewLockedValidator, ViewUniqueURIValidator)

    check_permissions(view, element, user)

    if element.get('errors'):
        return view

    if save:
        logger.info(_msg)
        view.save()
        set_m2m_instances(view, 'catalogs', element)
        view.sites.add(Site.objects.get_current())
        view.editors.add(Site.objects.get_current())

    return view
