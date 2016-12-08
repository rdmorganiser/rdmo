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
        self._text_element(xml, 'dc:description', {}, attribute["description"])
        self._text_element(xml, 'dc:uri', {}, attribute["uri"])
        self._text_element(xml, 'is_collection', {}, attribute["is_collection"])
        self._text_element(xml, 'value_type', {}, attribute["value_type"])
        self._text_element(xml, 'unit', {}, attribute["unit"])

        if 'options' in attribute and attribute['options']:
            xml.startElement('Options', {})

            for option in attribute['options']:
                self._option(xml, option)

            xml.endElement('Options')

        if 'range' in attribute and attribute['range']:
            self._range(xml, attribute['range'])

        if 'conditions' in attribute and attribute['conditions']:
            xml.startElement('Conditions', {})

            for conditions in attribute['conditions']:
                self._conditions(xml, conditions)

            xml.endElement('Conditions')

        if 'verbosename' in attribute and attribute['verbosename']:
            self._verbosename(xml, attribute['verbosename'])

        xml.endElement('Attribute')

    def _attribute_entity(self, xml, attribute_entity):
        xml.startElement('AttributeEntity', {})
        self._text_element(xml, 'dc:title', {}, attribute_entity["title"])
        self._text_element(xml, 'dc:description', {}, attribute_entity["description"])
        self._text_element(xml, 'dc:uri', {}, attribute_entity["uri"])
        self._text_element(xml, 'is_collection', {}, attribute_entity["is_collection"])

        if 'children' in attribute_entity:
            xml.startElement('Children', {})

            for child in attribute_entity['children']:
                if child['is_attribute']:
                    self._attribute(xml, child)
                else:
                    self._attribute_entity(xml, child)

            xml.endElement('Children')

        if 'conditions' in attribute_entity and attribute_entity['conditions']:
            xml.startElement('Conditions', {})

            for conditions in attribute_entity['conditions']:
                self._conditions(xml, conditions)

            xml.endElement('Conditions')

        if 'verbosename' in attribute_entity and attribute_entity['verbosename']:
            self._verbosename(xml, attribute_entity['verbosename'])

        xml.endElement('AttributeEntity')

    def _option(self, xml, option):
        xml.startElement('Option', {})
        self._text_element(xml, 'order', {}, option["order"])
        self._text_element(xml, 'text_de', {}, option["text_de"])
        self._text_element(xml, 'text_en', {}, option["text_en"])
        self._text_element(xml, 'additional_input', {}, option["additional_input"])
        xml.endElement('Option')

    def _range(self, xml, range):
        xml.startElement('range', {})
        self._text_element(xml, 'minimum', {}, range["minimum"])
        self._text_element(xml, 'maximum', {}, range["maximum"])
        self._text_element(xml, 'step', {}, range["step"])
        xml.endElement('range')

    def _conditions(self, xml, conditions):
        xml.startElement('condition', {})
        self._text_element(xml, 'source', {}, conditions["source"])
        self._text_element(xml, 'relation', {}, conditions["relation"])
        self._text_element(xml, 'target_text', {}, conditions["target_text"])
        self._text_element(xml, 'target_option', {}, conditions["target_option"])
        xml.endElement('condition')

    def _verbosename(self, xml, verbosename):
        xml.startElement('verbosename', {})
        self._text_element(xml, 'name_en', {}, verbosename["name_en"])
        self._text_element(xml, 'name_de', {}, verbosename["name_de"])
        self._text_element(xml, 'name_plural_en', {}, verbosename["name_plural_en"])
        self._text_element(xml, 'name_plural_de', {}, verbosename["name_plural_de"])
        xml.endElement('verbosename')

    def _text_element(self, xml, tag, attributes, text):
        xml.startElement(tag, attributes)
        if text is not None:
            xml.characters(smart_text(text))
        xml.endElement(tag)
