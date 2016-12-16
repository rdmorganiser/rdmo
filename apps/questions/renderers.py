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
        xml.startElement('Catalogs', {})

        for catalog in data:
            self._catalog(xml, catalog)

        xml.endElement('Catalogs')
        xml.endDocument()
        return stream.getvalue()

    def _catalog(self, xml, catalog):
        xml.startElement('Catalog', {})
        self._text_element(xml, 'title', {}, catalog["title"])
        self._text_element(xml, 'order', {}, catalog["order"])

        if 'sections' in catalog and catalog['sections']:
            xml.startElement('Sections', {})

            for section in catalog['sections']:
                self._section(xml, section)

            xml.endElement('Sections')

        xml.endElement('Catalog')

    def _section(self, xml, section):
        xml.startElement('Section', {})
        self._text_element(xml, 'order', {}, section["order"])
        self._text_element(xml, 'title_en', {}, section["title_en"])
        self._text_element(xml, 'title_de', {}, section["title_de"])

        if 'subsections' in section and section['subsections']:
            xml.startElement('Subsections', {})

            for subsection in section['subsections']:
                self._subsection(xml, subsection)

            xml.endElement('Subsections')

        xml.endElement('Section')

    def _subsection(self, xml, subsection):
        xml.startElement('Subsection', {})
        self._text_element(xml, 'order', {}, subsection["order"])
        self._text_element(xml, 'title_en', {}, subsection["title_en"])
        self._text_element(xml, 'title_de', {}, subsection["title_de"])

        if 'entities' in subsection and subsection['entities']:
            xml.startElement('QuestionEntities', {})

            for questionentity in subsection['entities']:
                if 'is_set' in questionentity and questionentity['is_set']:
                    self._questionset(xml, questionentity)
                else:
                    self._question(xml, questionentity)

            xml.endElement('QuestionEntities')

        xml.endElement('Subsection')

    def _question(self, xml, question):
        xml.startElement('Question', {})
        self._text_element(xml, 'text_en', {}, question["text_en"])
        self._text_element(xml, 'text_de', {}, question["text_de"])
        self._text_element(xml, 'attribute_entity', {}, question["attribute_entity"]['label'])
        xml.endElement('Question')

    def _questionset(self, xml, questionset):
        xml.startElement('QuestionSet', {})
        self._text_element(xml, 'order', {}, questionset["order"])
        self._text_element(xml, 'help_en', {}, questionset["help_en"])
        self._text_element(xml, 'help_de', {}, questionset["help_de"])
        xml.startElement('Questions', {})

        for question in questionset['questions']:
            self._question(xml, question)

        xml.endElement('Questions')
        xml.endElement('QuestionSet')

    def _text_element(self, xml, tag, questionentity, text):
        xml.startElement(tag, questionentity)
        if text is not None:
            xml.characters(smart_text(text))
        xml.endElement(tag)
