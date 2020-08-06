from xml.dom.minidom import parseString

from django.http import HttpResponse


class XMLResponse(HttpResponse):

    def __init__(self, xml, file_name=None):
        super().__init__(prettify_xml(xml), content_type='application/xml')
        if file_name:
            self['Content-Disposition'] = 'filename="{}"'.format(file_name)


def prettify_xml(xmlstring):
    xmlobj = parseString(xmlstring)
    return xmlobj.toprettyxml()
