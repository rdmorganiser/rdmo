import logging

from rdmo.core.utils import get_ns_map, get_ns_tag

from .models import View

log = logging.getLogger(__name__)


def import_views(views_node):
    log.info('Importing views')
    nsmap = get_ns_map(views_node.getroot())

    for view_node in views_node.findall('view'):
        view_uri = view_node.find(get_ns_tag('dc:uri', nsmap)).text

        try:
            view = View.objects.get(uri=view_uri)
        except View.DoesNotExist:
            view = View()
            log.info('View not in db. Created with uri ' + view_uri)
        else:
            log.info('View does exist. Loaded from uri ' + view_uri)

        view.uri_prefix = view_uri.split('/views/')[0]
        view.key = view_uri.split('/')[-1]

        for element in view_node.findall('title'):
            setattr(view, 'title_' + element.attrib['lang'], element.text)
        for element in view_node.findall('help'):
            setattr(view, 'help_' + element.attrib['lang'], element.text)

        view.template = view_node.find('template').text
        view.save()
