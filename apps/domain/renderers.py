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
        xml.startElement('AttributeEntities', {})

        for attribute_entity in data:
            if attribute_entity["is_set"]:
                xml.startElement('AttributeSet', {
                    'tag': attribute_entity["tag"],
                    'is_collection': str(attribute_entity["is_collection"])
                })

                for set_entity in attribute_entity["attributes"]:
                    xml.startElement('Attribute', {
                        'tag': set_entity["tag"],
                        'is_collection': str(set_entity["is_collection"]),
                        'value_type': set_entity["value_type"]
                    })

                    xml.endElement('Attribute')
                xml.endElement('AttributeSet')

            if attribute_entity["is_set"] == 0:
                xml.startElement('Attribute', {
                    'tag': attribute_entity["tag"],
                    'is_collection': str(attribute_entity["is_collection"])
                })

                xml.endElement('Attribute')

        xml.endElement('AttributeEntities')
        xml.endDocument()
        return stream.getvalue()
