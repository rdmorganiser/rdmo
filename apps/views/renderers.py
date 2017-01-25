from __future__ import unicode_literals

from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.six.moves import StringIO
from django.utils.encoding import smart_text
from rest_framework.renderers import BaseRenderer


class XMLRenderer(BaseRenderer):

    media_type = 'application/xml'
    format = 'xml'

    def render(self, data):

        if data is None:
            return ''

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, "utf-8")
        xml.startDocument()
        xml.startElement('views', {})

        for view in data:
            self._view(xml, view)

        xml.endElement('views')
        xml.endDocument()
        return stream.getvalue()

    def _view(self, xml, view):
        xml.startElement('view', {})
        self._text_element(xml, 'identifier', {}, view["identifier"])
        self._text_element(xml, 'uri', {}, view["uri"])
        self._text_element(xml, 'comment', {}, view["comment"])
        self._text_element(xml, 'template', {}, view["template"])
        xml.endElement('view')

    def _text_element(self, xml, tag, view, text):
        xml.startElement(tag, view)
        if text is not None:
            xml.characters(smart_text(text))
        xml.endElement(tag)
