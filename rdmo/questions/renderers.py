from rdmo.core.renderers import BaseXMLRenderer
from rdmo.core.utils import get_languages


class XMLRenderer(BaseXMLRenderer):

    def render_catalog(self, xml, catalog):
        xml.startElement('catalog', {'dc:uri': catalog['uri']})
        self.render_text_element(xml, 'uri_prefix', {}, catalog['uri_prefix'])
        self.render_text_element(xml, 'uri_path', {}, catalog['uri_path'])
        self.render_text_element(xml, 'dc:comment', {}, catalog['comment'])
        self.render_text_element(xml, 'order', {}, catalog['order'])

        for lang_code, lang_string, lang_field in get_languages():
            self.render_text_element(xml, 'title', {'lang': lang_code}, catalog['title_%s' % lang_code])
            self.render_text_element(xml, 'help', {'lang': lang_code}, catalog['help_%s' % lang_code])

        xml.startElement('sections', {})
        for catalog_section in catalog['catalog_sections']:
            self.render_text_element(xml, 'section', {
                'dc:uri': catalog_section['section']['uri'],
                'order': str(catalog_section['order'])
            }, None)
        xml.endElement('sections')

        xml.endElement('catalog')

        for section in catalog['catalog_sections']:
            self.render_section(xml, section.get('section'))

    def render_section(self, xml, section):
        xml.startElement('section', {'dc:uri': section['uri']})
        self.render_text_element(xml, 'uri_prefix', {}, section['uri_prefix'])
        self.render_text_element(xml, 'uri_path', {}, section['uri_path'])
        self.render_text_element(xml, 'dc:comment', {}, section['comment'])

        for lang_code, lang_string, lang_field in get_languages():
            self.render_text_element(xml, 'title', {'lang': lang_code}, section['title_%s' % lang_code])

        xml.startElement('pages', {})
        for section_page in section['section_pages']:
            self.render_text_element(xml, 'page', {
                'dc:uri': section_page['page']['uri'],
                'order': str(section_page['order'])
            }, None)
        xml.endElement('pages')

        xml.endElement('section')

        for section_page in section['section_pages']:
            self.render_page(xml, section_page.get('page'))

    def render_page(self, xml, page):
        xml.startElement('page', {'dc:uri': page['uri']})
        self.render_text_element(xml, 'uri_prefix', {}, page['uri_prefix'])
        self.render_text_element(xml, 'uri_path', {}, page['uri_path'])
        self.render_text_element(xml, 'dc:comment', {}, page['comment'])
        self.render_text_element(xml, 'attribute', {'dc:uri': page['attribute']}, None)
        self.render_text_element(xml, 'is_collection', {}, page['is_collection'])

        for lang_code, lang_string, lang_field in get_languages():
            self.render_text_element(xml, 'title', {'lang': lang_code}, page['title_%s' % lang_code])
            self.render_text_element(xml, 'help', {'lang': lang_code}, page['help_%s' % lang_code])
            self.render_text_element(xml, 'verbose_name', {'lang': lang_code}, page['verbose_name_%s' % lang_code])
            self.render_text_element(xml, 'verbose_name_plural', {'lang': lang_code}, page['verbose_name_plural_%s' % lang_code])

        xml.startElement('questionsets', {})
        for page_questionset in page['page_questionsets']:
            self.render_text_element(xml, 'questionset', {
                'dc:uri': page_questionset['questionset']['uri'],
                'order': str(page_questionset['order'])
            }, None)
        xml.endElement('questionsets')

        xml.startElement('questions', {})
        for page_question in page['page_questions']:
            self.render_text_element(xml, 'question', {
                'dc:uri': page_question['question']['uri'],
                'order': str(page_question['order'])
            }, None)
        xml.endElement('questions')

        xml.startElement('conditions', {})
        for condition in page['conditions']:
            self.render_text_element(xml, 'condition', {'dc:uri': condition}, None)
        xml.endElement('conditions')

        xml.endElement('page')

        # for page_questionset in page['page_questionsets']:
        #     self.render_questionset(xml, page_questionset['questionset'])

        for page_question in page['page_questions']:
            self.render_question(xml, page_question['question'])

    def render_questionset(self, xml, questionset):
        xml.startElement('questionset', {'dc:uri': questionset['uri']})
        self.render_text_element(xml, 'uri_prefix', {}, questionset['uri_prefix'])
        self.render_text_element(xml, 'uri_path', {}, questionset['uri_path'])
        self.render_text_element(xml, 'dc:comment', {}, questionset['comment'])
        self.render_text_element(xml, 'attribute', {'dc:uri': questionset['attribute']}, None)
        self.render_text_element(xml, 'is_collection', {}, questionset['is_collection'])

        for lang_code, lang_string, lang_field in get_languages():
            self.render_text_element(xml, 'title', {'lang': lang_code}, questionset['title_%s' % lang_code])
            self.render_text_element(xml, 'help', {'lang': lang_code}, questionset['help_%s' % lang_code])
            self.render_text_element(xml, 'verbose_name', {'lang': lang_code}, questionset['verbose_name_%s' % lang_code])
            self.render_text_element(xml, 'verbose_name_plural', {'lang': lang_code}, questionset['verbose_name_plural_%s' % lang_code])

        xml.startElement('questionsets', {})
        for questionset_questionset in questionset['questionset_questionsets']:
            self.render_text_element(xml, 'questionset', {
                'dc:uri':  questionset_questionset['questionset']['uri'],
                'order': str(questionset_questionset['order'])
            }, None)
        xml.endElement('questionsets')

        xml.startElement('questions', {})
        for questionset_question in questionset['questionset_questions']:
            self.render_text_element(xml, 'question', {
                'dc:uri': questionset_question['question']['uri'],
                'order': str(questionset_question['order'])
            }, None)
        xml.endElement('questions')

        xml.startElement('conditions', {})
        for condition in questionset['conditions']:
            self.render_text_element(xml, 'condition', {'dc:uri': condition}, None)
        xml.endElement('conditions')

        xml.endElement('questionset')

        for questionset_questionset in questionset['questionset_questionsets']:
            self.render_questionset(xml, questionset_questionset['questionset'])

        for questionset_question in questionset['questionset_questions']:
            self.render_question(xml, questionset_question['question'])

    def render_question(self, xml, question):
        xml.startElement('question', {'dc:uri': question['uri']})
        self.render_text_element(xml, 'uri_prefix', {}, question['uri_prefix'])
        self.render_text_element(xml, 'uri_path', {}, question['uri_path'])
        self.render_text_element(xml, 'dc:comment', {}, question['comment'])
        self.render_text_element(xml, 'attribute', {'dc:uri': question['attribute']}, None)
        self.render_text_element(xml, 'is_collection', {}, question['is_collection'])
        self.render_text_element(xml, 'is_optional', {}, question['is_optional'])

        for lang_code, lang_string, lang_field in get_languages():
            self.render_text_element(xml, 'help', {'lang': lang_code}, question['help_%s' % lang_code])
            self.render_text_element(xml, 'text', {'lang': lang_code}, question['text_%s' % lang_code])
            self.render_text_element(xml, 'default_text', {'lang': lang_code}, question['default_text_%s' % lang_code])
            self.render_text_element(xml, 'verbose_name', {'lang': lang_code}, question['verbose_name_%s' % lang_code])
            self.render_text_element(xml, 'verbose_name_plural', {'lang': lang_code}, question['verbose_name_plural_%s' % lang_code])

        self.render_text_element(xml, 'default_option', {'dc:uri': question['default_option']}, None)
        self.render_text_element(xml, 'default_external_id', {}, question['default_external_id'])

        self.render_text_element(xml, 'widget_type', {}, question['widget_type'])
        self.render_text_element(xml, 'value_type', {}, question['value_type'])
        self.render_text_element(xml, 'maximum', {}, question['maximum'])
        self.render_text_element(xml, 'minimum', {}, question['minimum'])
        self.render_text_element(xml, 'step', {}, question['step'])
        self.render_text_element(xml, 'unit', {}, question['unit'])
        self.render_text_element(xml, 'width', {}, question['width'])

        xml.startElement('optionsets', {})
        for optionset in question['optionsets']:
            self.render_text_element(xml, 'optionset', {'dc:uri': optionset}, None)
        xml.endElement('optionsets')

        xml.startElement('conditions', {})
        for condition in question['conditions']:
            self.render_text_element(xml, 'condition', {'dc:uri': condition}, None)
        xml.endElement('conditions')

        xml.endElement('question')


class CatalogRenderer(XMLRenderer):

    def render_document(self, xml, catalogs):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'created': self.created
        })
        for catalog in catalogs:
            self.render_catalog(xml, catalog)
        xml.endElement('rdmo')


class SectionRenderer(XMLRenderer):

    def render_document(self, xml, sections):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'created': self.created
        })
        for section in sections:
            self.render_section(xml, section)
        xml.endElement('rdmo')


class PageRenderer(XMLRenderer):

    def render_document(self, xml, pages):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'created': self.created
        })
        for page in pages:
            self.render_page(xml, page)
        xml.endElement('rdmo')


class QuestionSetRenderer(XMLRenderer):

    def render_document(self, xml, questionsets):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'created': self.created
        })
        for questionset in questionsets:
            self.render_questionset(xml, questionset)
        xml.endElement('rdmo')


class QuestionRenderer(XMLRenderer):

    def render_document(self, xml, questions):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'created': self.created
        })
        for question in questions:
            self.render_question(xml, question)
        xml.endElement('rdmo')
