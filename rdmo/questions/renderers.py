from rdmo.core.renderers import BaseXMLRenderer


class XMLRenderer(BaseXMLRenderer):

    def render_document(self, xml, catalog):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/'
        })
        self.redner_catalog(xml, catalog)
        xml.endElement('rdmo')

    def redner_catalog(self, xml, catalog):
        xml.startElement('catalog', {})
        self.render_text_element(xml, 'dc:uri', {}, catalog['uri'])
        self.render_text_element(xml, 'dc:comment', {}, catalog['comment'])
        self.render_text_element(xml, 'order', {}, catalog['order'])
        self.render_text_element(xml, 'title', {'lang': 'en'}, catalog['title_en'])
        self.render_text_element(xml, 'title', {'lang': 'de'}, catalog['title_de'])
        xml.endElement('catalog')

        if 'sections' in catalog and catalog['sections']:
            for section in catalog['sections']:
                self.render_section(xml, section)

    def render_section(self, xml, section):
        xml.startElement('section', {})
        self.render_text_element(xml, 'dc:uri', {}, section['uri'])
        self.render_text_element(xml, 'dc:comment', {}, section['comment'])
        self.render_text_element(xml, 'catalog', {'dc:uri': section['catalog']}, None)
        self.render_text_element(xml, 'order', {}, section['order'])
        self.render_text_element(xml, 'title', {'lang': 'en'}, section['title_en'])
        self.render_text_element(xml, 'title', {'lang': 'de'}, section['title_de'])
        xml.endElement('section')

        if 'subsections' in section and section['subsections']:
            for subsection in section['subsections']:
                self.render_subsection(xml, subsection)

    def render_subsection(self, xml, subsection):
        xml.startElement('subsection', {})
        self.render_text_element(xml, 'dc:uri', {}, subsection['uri'])
        self.render_text_element(xml, 'dc:comment', {}, subsection['comment'])
        self.render_text_element(xml, 'section', {'dc:uri': subsection['section']}, None)
        self.render_text_element(xml, 'order', {}, subsection['order'])
        self.render_text_element(xml, 'title', {'lang': 'en'}, subsection['title_en'])
        self.render_text_element(xml, 'title', {'lang': 'de'}, subsection['title_de'])
        xml.endElement('subsection')

        if 'questionsets' in subsection and subsection['questionsets']:
            for questionset in subsection['questionsets']:
                self.render_questionset(xml, questionset)

    def render_questionset(self, xml, questionset):
        xml.startElement('questionset', {})
        self.render_text_element(xml, 'dc:uri', {}, questionset['uri'])
        self.render_text_element(xml, 'dc:comment', {}, questionset['comment'])
        self.render_text_element(xml, 'attribute', {'dc:uri': questionset['attribute']}, None)
        self.render_text_element(xml, 'subsection', {'dc:uri': questionset['subsection']}, None)
        self.render_text_element(xml, 'is_collection', {}, questionset['is_collection'])
        self.render_text_element(xml, 'order', {}, questionset['order'])
        self.render_text_element(xml, 'help', {'lang': 'en'}, questionset['help_en'])
        self.render_text_element(xml, 'help', {'lang': 'de'}, questionset['help_de'])
        self.render_text_element(xml, 'verbose_name', {'lang': 'en'}, questionset['verbose_name_en'])
        self.render_text_element(xml, 'verbose_name', {'lang': 'de'}, questionset['verbose_name_de'])
        self.render_text_element(xml, 'verbose_name_plural', {'lang': 'en'}, questionset['verbose_name_plural_en'])
        self.render_text_element(xml, 'verbose_name_plural', {'lang': 'de'}, questionset['verbose_name_plural_de'])

        if 'conditions' in questionset and questionset['conditions']:
            xml.startElement('conditions', {})
            for condition in questionset['conditions']:
                self.render_text_element(xml, 'condition', {'dc:uri': condition}, None)
            xml.endElement('conditions')

        xml.endElement('questionset')

        if 'questions' in questionset and questionset['questions']:
            for question in questionset['questions']:
                self.render_question(xml, question)

    def render_question(self, xml, question):
        xml.startElement('question', {})
        self.render_text_element(xml, 'dc:uri', {}, question['uri'])
        self.render_text_element(xml, 'dc:comment', {}, question['comment'])
        self.render_text_element(xml, 'attribute', {'dc:uri': question['attribute']}, None)
        self.render_text_element(xml, 'questionset', {'dc:uri': question['questionset']}, None)
        self.render_text_element(xml, 'is_collection', {}, question['is_collection'])
        self.render_text_element(xml, 'order', {}, question['order'])
        self.render_text_element(xml, 'help', {'lang': 'en'}, question['help_en'])
        self.render_text_element(xml, 'help', {'lang': 'de'}, question['help_de'])
        self.render_text_element(xml, 'text', {'lang': 'en'}, question['text_en'])
        self.render_text_element(xml, 'text', {'lang': 'de'}, question['text_de'])
        self.render_text_element(xml, 'verbose_name', {'lang': 'en'}, question['verbose_name_en'])
        self.render_text_element(xml, 'verbose_name', {'lang': 'de'}, question['verbose_name_de'])
        self.render_text_element(xml, 'verbose_name_plural', {'lang': 'en'}, question['verbose_name_plural_en'])
        self.render_text_element(xml, 'verbose_name_plural', {'lang': 'de'}, question['verbose_name_plural_de'])
        self.render_text_element(xml, 'widget_type', {}, question['widget_type'])
        self.render_text_element(xml, 'value_type', {}, question['value_type'])
        self.render_text_element(xml, 'maximum', {}, question['maximum'])
        self.render_text_element(xml, 'minimum', {}, question['minimum'])
        self.render_text_element(xml, 'step', {}, question['step'])
        self.render_text_element(xml, 'unit', {}, question['unit'])

        if 'optionsets' in question and question['optionsets']:
            xml.startElement('optionsets', {})
            for optionset in question['optionsets']:
                self.render_text_element(xml, 'optionset', {'dc:uri': optionset}, None)
            xml.endElement('optionsets')

        if 'conditions' in question and question['conditions']:
            xml.startElement('conditions', {})
            for condition in question['conditions']:
                self.render_text_element(xml, 'condition', {'dc:uri': condition}, None)
            xml.endElement('conditions')

        xml.endElement('question')
