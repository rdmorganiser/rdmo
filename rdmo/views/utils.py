from lxml import etree

from rdmo.core.utils import get_ns_tag
from rdmo.domain.models import AttributeEntity

from .models import View


def import_views(views_node):

    nsmap = views_node.nsmap

    for view_node in views_node.iterchildren():
        view_uri = view_node[get_ns_tag('dc:uri', nsmap)].text

        try:
            view = View.objects.get(uri=view_uri)
        except View.DoesNotExist:
            view = View()

        view.uri_prefix = view_uri.split('/views/')[0]
        view.key = view_uri.split('/')[-1]

        for element in view_node['title']:
            setattr(view, 'title_' + element.get('lang'), element.text)
        for element in view_node['help']:
            setattr(view, 'help_' + element.get('lang'), element.text)

        view.template = view_node['template'].text
        view.save()
