import logging

from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from rdmo.core.imports import set_lang_field
from rdmo.core.utils import get_languages
from rdmo.core.xml import filter_elements_by_type, flat_xml_to_elements
from rdmo.questions.models import Catalog

from .models import View
from .validators import ViewUniqueKeyValidator

log = logging.getLogger(__name__)


def import_views(root):
    elements = flat_xml_to_elements(root)

    for element in filter_elements_by_type(elements, 'view'):
        import_view(element)


def import_view(element):
    try:
        view = View.objects.get(uri=element['uri'])
    except View.DoesNotExist:
        log.info('View not in db. Created with uri %s.', element['uri'])
        view = View()

    view.uri_prefix = element['uri_prefix'] or ''
    view.key = element['key'] or ''
    view.comment = element['comment'] or ''

    view.template = element['template'] or ''

    for lang_code, lang_string, lang_field in get_languages():
        set_lang_field(view, 'title', element, lang_code, lang_field)
        set_lang_field(view, 'help', element, lang_code, lang_field)

    try:
        ViewUniqueKeyValidator(view).validate()
    except ValidationError as e:
        log.info('View not saving "%s" due to validation error (%s).', element['uri'], e)
        pass
    else:
        log.info('View saving to "%s".', element['uri'])
        view.save()
        view.sites.add(Site.objects.get_current())

        for catalog_uri in element.get('catalogs', []):
            try:
                view.catalogs.add(Catalog.objects.get(uri=catalog_uri))
            except Catalog.DoesNotExist:
                pass
