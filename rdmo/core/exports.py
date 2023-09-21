from xml.dom.minidom import parseString

from django.conf import settings
from django.http import HttpResponse


class XMLResponse(HttpResponse):

    def __init__(self, xml, name=None):
        super().__init__(prettify_xml(xml), content_type='application/xml')
        if name and settings.EXPORT_CONTENT_DISPOSITION == 'attachment':
            self['Content-Disposition'] = 'attachment; filename="{}.xml"'.format(name.replace('/', '_'))


def prettify_xml(xmlstring):
    xmlobj = parseString(xmlstring)
    return xmlobj.toprettyxml(
        indent='\t', newl='\n', encoding='UTF-8'
    )
