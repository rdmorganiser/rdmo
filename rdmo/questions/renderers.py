from rdmo.core.renderers import BaseXMLRenderer


class XMLRenderer(BaseXMLRenderer):

    def render_document(self, xml, catalog):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/'
        })
        self.render_catalog(xml, catalog)
        xml.endElement('rdmo')

    def render_catalog(self, xml, catalog):
        xml.startElement('catalog', {'dc:uri': catalog['uri']})
        self.render_text_element(xml, 'uri_prefix', {}, catalog['uri_prefix'])
        self.render_text_element(xml, 'key', {}, catalog['key'])
        self.render_text_element(xml, 'dc:comment', {}, catalog['comment'])
        self.render_text_element(xml, 'order', {}, catalog['order'])
        self.render_text_element(xml, 'title', {'lang': 'en'}, catalog['title_en'])
        self.render_text_element(xml, 'title', {'lang': 'de'}, catalog['title_de'])
        xml.endElement('catalog')

        if 'sections' in catalog and catalog['sections']:
            for section in catalog['sections']:
                self.render_section(xml, section)

    def render_section(self, xml, section):
        xml.startElement('section', {'dc:uri': section['uri']})
        self.render_text_element(xml, 'uri_prefix', {}, section['uri_prefix'])
        self.render_text_element(xml, 'key', {}, section['key'])
        self.render_text_element(xml, 'path', {}, section['path'])
        self.render_text_element(xml, 'dc:comment', {}, section['comment'])
        self.render_text_element(xml, 'catalog', {'dc:uri': section['catalog']}, None)
        self.render_text_element(xml, 'order', {}, section['order'])
        self.render_text_element(xml, 'title', {'lang': 'en'}, section['title_en'])
        self.render_text_element(xml, 'title', {'lang': 'de'}, section['title_de'])
        xml.endElement('section')

        if 'questionsets' in section and section['questionsets']:
            for questionset in section['questionsets']:
                self.render_questionset(xml, questionset)

    def render_questionset(self, xml, questionset):
        xml.startElement('questionset', {'dc:uri': questionset['uri']})
        self.render_text_element(xml, 'uri_prefix', {}, questionset['uri_prefix'])
        self.render_text_element(xml, 'key', {}, questionset['key'])
        self.render_text_element(xml, 'path', {}, questionset['path'])
        self.render_text_element(xml, 'dc:comment', {}, questionset['comment'])
        self.render_text_element(xml, 'attribute', {'dc:uri': questionset['attribute']}, None)
        self.render_text_element(xml, 'section', {'dc:uri': questionset['section']}, None)
        self.render_text_element(xml, 'is_collection', {}, questionset['is_collection'])
        self.render_text_element(xml, 'order', {}, questionset['order'])
        self.render_text_element(xml, 'title', {'lang': 'en'}, questionset['title_en'])
        self.render_text_element(xml, 'title', {'lang': 'de'}, questionset['title_de'])
        self.render_text_element(xml, 'help', {'lang': 'en'}, questionset['help_en'])
        self.render_text_element(xml, 'help', {'lang': 'de'}, questionset['help_de'])
        self.render_text_element(xml, 'verbose_name', {'lang': 'en'}, questionset['verbose_name_en'])
        self.render_text_element(xml, 'verbose_name', {'lang': 'de'}, questionset['verbose_name_de'])
        self.render_text_element(xml, 'verbose_name_plural', {'lang': 'en'}, questionset['verbose_name_plural_en'])
        self.render_text_element(xml, 'verbose_name_plural', {'lang': 'de'}, questionset['verbose_name_plural_de'])

        xml.startElement('conditions', {})
        if 'conditions' in questionset and questionset['conditions']:
            for condition in questionset['conditions']:
                self.render_text_element(xml, 'condition', {'dc:uri': condition}, None)
        xml.endElement('conditions')

        xml.endElement('questionset')

        if 'questions' in questionset and questionset['questions']:
            for question in questionset['questions']:
                self.render_question(xml, question)

    def render_question(self, xml, question):
        xml.startElement('question', {'dc:uri': question['uri']})
        self.render_text_element(xml, 'uri_prefix', {}, question['uri_prefix'])
        self.render_text_element(xml, 'key', {}, question['key'])
        self.render_text_element(xml, 'path', {}, question['path'])
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

        xml.startElement('optionsets', {})
        if 'optionsets' in question and question['optionsets']:
            for optionset in question['optionsets']:
                self.render_text_element(xml, 'optionset', {'dc:uri': optionset}, None)
        xml.endElement('optionsets')

        xml.startElement('conditions', {})
        if 'conditions' in question and question['conditions']:
            for condition in question['conditions']:
                self.render_text_element(xml, 'condition', {'dc:uri': condition}, None)
        xml.endElement('conditions')

        xml.endElement('question')
