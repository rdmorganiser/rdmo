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
            if attribute_entity['is_attribute']:
                self._attribute(xml, attribute_entity)
            else:
                self._attribute_entity(xml, attribute_entity)

        xml.endElement('Domain')
        xml.endDocument()
        return stream.getvalue()

    def _attribute(self, xml, attribute):
        xml.startElement('Attribute', {})
        self._text_element(xml, 'dc:title', {}, attribute["title"])
        self._text_element(xml, 'description', {}, attribute["description"])
        self._text_element(xml, 'uri', {}, attribute["uri"])
        self._text_element(xml, 'is_collection', {}, attribute["is_collection"])
        self._text_element(xml, 'value_type', {}, attribute["value_type"])
        self._text_element(xml, 'unit', {}, attribute["unit"])
        # self._text_element(xml, 'verbosename', {}, attribute["verbosename"])

        if 'options' in attribute and attribute['options']:
            xml.startElement('Options', {})

            for option in attribute['options']:
                self._option(xml, option)

            xml.endElement('Options')

        xml.endElement('Attribute')

    def _attribute_entity(self, xml, attribute_entity):
        xml.startElement('AttributeEntity', {})
        self._text_element(xml, 'dc:title', {}, attribute_entity["title"])
        self._text_element(xml, 'description', {}, attribute_entity["description"])
        self._text_element(xml, 'uri', {}, attribute_entity["uri"])
        self._text_element(xml, 'is_collection', {}, attribute_entity["is_collection"])
        # self._text_element(xml, 'range', {}, attribute_entity["range"])
        # self._text_element(xml, 'verbosename', {}, attribute_entity["verbosename"])

        if 'children' in attribute_entity:
            xml.startElement('Children', {})

            for child in attribute_entity['children']:
                if child['is_attribute']:
                    self._attribute(xml, child)
                else:
                    self._attribute_entity(xml, child)

            xml.endElement('Children')

        xml.endElement('AttributeEntity')

    def _option(self, xml, option):
        xml.startElement('Option', {})
        self._text_element(xml, 'order', {}, option["order"])
        self._text_element(xml, 'text_de', {}, option["text_de"])
        self._text_element(xml, 'text_en', {}, option["text_en"])
        self._text_element(xml, 'additional_input', {}, option["additional_input"])

        xml.endElement('Option')

    def _text_element(self, xml, tag, attributes, text):
        xml.startElement(tag, attributes)
        xml.characters(smart_text(text))
        xml.endElement(tag)
