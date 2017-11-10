from rdmo.core.renderers import BaseXMLRenderer


class XMLRenderer(BaseXMLRenderer):

    def render_document(self, xml, catalog):
        xml.startElement('catalog', {
            'xmlns:dc': "http://purl.org/dc/elements/1.1/"
        })
        self.render_text_element(xml, 'dc:uri', {}, catalog["uri"])
        self.render_text_element(xml, 'dc:comment', {}, catalog["comment"])
        self.render_text_element(xml, 'order', {}, catalog["order"])
        self.render_text_element(xml, 'title', {'lang': 'en'}, catalog["title_en"])
        self.render_text_element(xml, 'title', {'lang': 'de'}, catalog["title_de"])

        if 'sections' in catalog and catalog['sections']:
            xml.startElement('sections', {})
            for section in catalog['sections']:
                self.render_section(xml, section)
            xml.endElement('sections')

        xml.endElement('catalog')

    def render_section(self, xml, section):
        xml.startElement('section', {})
        self.render_text_element(xml, 'dc:uri', {}, section["uri"])
        self.render_text_element(xml, 'dc:comment', {}, section["comment"])
        self.render_text_element(xml, 'order', {}, section["order"])
        self.render_text_element(xml, 'title', {'lang': 'en'}, section["title_en"])
        self.render_text_element(xml, 'title', {'lang': 'de'}, section["title_de"])

        if 'subsections' in section and section['subsections']:
            xml.startElement('subsections', {})
            for subsection in section['subsections']:
                self.render_subsection(xml, subsection)
            xml.endElement('subsections')

        xml.endElement('section')

    def render_subsection(self, xml, subsection):
        xml.startElement('subsection', {})
        self.render_text_element(xml, 'dc:uri', {}, subsection["uri"])
        self.render_text_element(xml, 'dc:comment', {}, subsection["comment"])
        self.render_text_element(xml, 'order', {}, subsection["order"])
        self.render_text_element(xml, 'title', {'lang': 'en'}, subsection["title_en"])
        self.render_text_element(xml, 'title', {'lang': 'de'}, subsection["title_de"])

        if 'entities' in subsection and subsection['entities']:
            xml.startElement('entities', {})
            for questionentity in subsection['entities']:
                if 'is_set' in questionentity and questionentity['is_set']:
                    self.render_questionset(xml, questionentity)
                else:
                    self.render_question(xml, questionentity)
            xml.endElement('entities')

        xml.endElement('subsection')

    def render_question(self, xml, question):
        xml.startElement('question', {})
        self.render_text_element(xml, 'dc:uri', {}, question["uri"])
        self.render_text_element(xml, 'dc:comment', {}, question["comment"])
        self.render_text_element(xml, 'order', {}, question["order"])
        self.render_text_element(xml, 'text', {'lang': 'en'}, question["text_en"])
        self.render_text_element(xml, 'text', {'lang': 'de'}, question["text_de"])
        self.render_text_element(xml, 'help', {'lang': 'en'}, question["help_en"])
        self.render_text_element(xml, 'help', {'lang': 'de'}, question["help_de"])
        self.render_text_element(xml, 'widget_type', {}, question["widget_type"])
        self.render_text_element(xml, 'attribute_entity', {'dc:uri': question["attribute_entity"]}, None)
        xml.endElement('question')

    def render_questionset(self, xml, questionset):
        xml.startElement('questionset', {})
        self.render_text_element(xml, 'dc:uri', {}, questionset["uri"])
        self.render_text_element(xml, 'dc:comment', {}, questionset["comment"])
        self.render_text_element(xml, 'order', {}, questionset["order"])
        self.render_text_element(xml, 'help', {'lang': 'en'}, questionset["help_en"])
        self.render_text_element(xml, 'help', {'lang': 'de'}, questionset["help_de"])
        self.render_text_element(xml, 'attribute_entity', {'dc:uri': questionset["attribute_entity"]}, None)

        xml.startElement('questions', {})
        for question in questionset['questions']:
            self.render_question(xml, question)
        xml.endElement('questions')

        xml.endElement('questionset')
