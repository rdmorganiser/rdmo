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
        xml.startElement('projects', {})

        for project in data:
            self._project(xml, project)

        xml.endElement('projects')
        xml.endDocument()
        return stream.getvalue()

    def _project(self, xml, project):
        xml.startElement('project', {})
        self._text_element(xml, 'title', {}, project["title"])
        self._text_element(xml, 'description', {}, project["description"])
        self._text_element(xml, 'catalog', {}, project["catalog"])

        if 'snapshots' in project and project['snapshots']:
            xml.startElement('snapshots', {})

            for snapshot in project['snapshots']:
                self._snapshot(xml, snapshot)

            xml.endElement('snapshots')

        if 'values' in project and project['values']:
            xml.startElement('values', {})

            for value in project['values']:
                self._value(xml, value)

            xml.endElement('values')

        xml.endElement('project')

    def _snapshot(self, xml, snapshot):
        xml.startElement('snapshot', {})
        self._text_element(xml, 'title', {}, snapshot["title"])
        self._text_element(xml, 'description', {}, snapshot["description"])
        self._text_element(xml, 'project', {}, snapshot["project"])

        if 'values' in snapshot and snapshot['values']:
            xml.startElement('values', {})

            for value in snapshot['values']:
                self._value(xml, value)

            xml.endElement('values')

        xml.endElement('snapshot')

    def _value(self, xml, value):
        xml.startElement('value', {})
        self._text_element(xml, 'created', {}, value["created"])
        self._text_element(xml, 'updated', {}, value["updated"])

        xml.startElement('attribute', value["attribute"])
        xml.endElement('attribute')

        self._text_element(xml, 'set_index', {}, value["set_index"])
        self._text_element(xml, 'collection_index', {}, value["collection_index"])
        self._text_element(xml, 'text', {}, value["text"])

        if value["option"]:
            xml.startElement('option', value["option"])
            xml.endElement('option')

        xml.endElement('value')

    def _text_element(self, xml, tag, value, text):
        xml.startElement(tag, value)
        if text is not None:
            xml.characters(smart_text(text))
        xml.endElement(tag)
