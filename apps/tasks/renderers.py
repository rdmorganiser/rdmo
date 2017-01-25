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
        xml.startElement('tasks', {})

        for task in data:
            self._task(xml, task)

        xml.endElement('tasks')
        xml.endDocument()
        return stream.getvalue()

    def _task(self, xml, task):
        xml.startElement('task', {})
        self._text_element(xml, 'identifier', {}, task["identifier"])
        self._text_element(xml, 'uri', {}, task["uri"])
        self._text_element(xml, 'attribute', {}, task["attribute"])
        self._text_element(xml, 'time_period', {}, task["time_period"])
        self._text_element(xml, 'title_en', {}, task["title_en"])
        self._text_element(xml, 'title_de', {}, task["title_de"])
        self._text_element(xml, 'text_en', {}, task["text_en"])
        self._text_element(xml, 'text_de', {}, task["text_de"])
        self._text_element(xml, 'conditions', {}, task["conditions"])
        xml.endElement('task')

    def _text_element(self, xml, tag, task, text):
        xml.startElement(tag, task)
        if text is not None:
            xml.characters(smart_text(text))
        xml.endElement(tag)
