from io import StringIO

from django.utils.encoding import smart_str
from django.utils.timezone import get_current_timezone, now
from django.utils.xmlutils import SimplerXMLGenerator

from rest_framework.renderers import BaseRenderer

from rdmo import __version__


class BaseXMLRenderer(BaseRenderer):

    media_type = 'application/xml'
    format = 'xml'

    def render(self, data, context={}):

        if data is None:
            return ''

        self.context = context
        self.uris = set()

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, "utf-8")
        xml.startDocument()
        self.render_document(xml, data)
        xml.endDocument()

        return stream.getvalue()

    def render_text_element(self, xml, tag, attrs, text):
        # remove None values from attrs
        attrs = {key: value for key, value in attrs.items() if value}

        xml.startElement(tag, attrs)
        if text is not None:
            xml.characters(smart_str(text))
        xml.endElement(tag)

    def render_document(self, xml, data):
        pass

    @property
    def version(self):
        return __version__

    @property
    def created(self):
        return now().astimezone(get_current_timezone()).isoformat()
