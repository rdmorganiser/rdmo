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
        self.render_document(xml, data)
        xml.endDocument()
        return stream.getvalue()

    def render_text_element(self, xml, tag, attrs, text):
        xml.startElement(tag, attrs)
        if text is not None:
            xml.characters(smart_text(text))
        xml.endElement(tag)

    def render_document(self, xml, optionsets):
        xml.startElement('options', {
            'xmlns:dc': "http://purl.org/dc/elements/1.1/"
        })

        for optionset in optionsets:
            self.render_optionset(xml, optionset)

        xml.endElement('options')

    def render_optionset(self, xml, optionset):
        xml.startElement('optionset', {})
        self.render_text_element(xml, 'dc:uri', {}, optionset["uri"])
        self.render_text_element(xml, 'dc:comment', {}, optionset["comment"])
        self.render_text_element(xml, 'order', {}, optionset["order"])

        if 'options' in optionset and optionset['options']:
            xml.startElement('options', {})

            for option in optionset['options']:
                self.render_option(xml, option)

            xml.endElement('options')

        if 'conditions' in optionset and optionset['conditions']:
            xml.startElement('conditions', {})

            for condition in optionset['conditions']:
                self.render_text_element(xml, 'condition', condition, None)

            xml.endElement('conditions')

        xml.endElement('optionset')

    def render_option(self, xml, option):
        xml.startElement('option', {})
        self.render_text_element(xml, 'dc:uri', {}, option["uri"])
        self.render_text_element(xml, 'dc:comment', {}, option["comment"])
        self.render_text_element(xml, 'order', {}, option["order"])
        self.render_text_element(xml, 'text', {'lang': 'en'}, option["text_en"])
        self.render_text_element(xml, 'text', {'lang': 'de'}, option["text_de"])
        self.render_text_element(xml, 'additional_input', {}, option["additional_input"])
        xml.endElement('option')
