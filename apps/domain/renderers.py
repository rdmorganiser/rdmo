"""
Provides XML rendering support.
"""
from __future__ import unicode_literals

from django.utils import six
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.six.moves import StringIO
from django.utils.encoding import smart_text
from rest_framework.renderers import BaseRenderer


class XMLRenderer(BaseRenderer):
    """
    Renderer which serializes to XML.
    """

    media_type = 'application/xml'
    format = 'xml'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders 'data' into serialized XML.
        """
        if data is None:
            return ''

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, "utf-8")
        xml.startDocument()
        xml.startElement('Domain', {
            'xmlns:dc': "http://purl.org/dc/elements/1.1/"
        })

        for attribute_entity in data:
            if attribute_entity["is_set"]:
                xml.startElement('AttributeSet', {
                    'dc:title': attribute_entity["tag"],
                    'is_collection': str(attribute_entity["is_collection"])
                })

                for set_entity in attribute_entity["attributes"]:
                    xml.startElement('Attribute', {
                        'is_collection': str(set_entity["is_collection"]),
                        'value_type': set_entity["value_type"]
                    })
                    xml.startElement('dc:title', {})
                    xml.characters(smart_text(set_entity["tag"]))
                    xml.endElement('dc:title')

                    xml.endElement('Attribute')
                xml.endElement('AttributeSet')

            else:
                xml.startElement('Attribute', {
                    'is_collection': str(attribute_entity["is_collection"])
                })
                xml.startElement('dc:title', {})
                xml.characters(smart_text(attribute_entity["tag"]))
                xml.endElement('dc:title')

                xml.endElement('Attribute')

        xml.endElement('Domain')
        xml.endDocument()
        return stream.getvalue()
