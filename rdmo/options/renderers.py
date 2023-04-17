from rdmo.core.renderers import BaseXMLRenderer
from rdmo.core.utils import get_languages


class OptionsRenderer(BaseXMLRenderer):

    def render_optionset(self, xml, optionset):
        xml.startElement('optionset', {'dc:uri': optionset['uri']})
        self.render_text_element(xml, 'uri_prefix', {}, optionset['uri_prefix'])
        self.render_text_element(xml, 'uri_path', {}, optionset['uri_path'])
        self.render_text_element(xml, 'dc:comment', {}, optionset['comment'])
        self.render_text_element(xml, 'provider_key', {}, optionset['provider_key'])

        xml.startElement('options', {})
        for optionset_option in optionset['optionset_options']:
            self.render_text_element(xml, 'option', {
                'dc:uri': optionset_option['option']['uri'],
                'order': str(optionset_option['order'])
            }, None)
        xml.endElement('options')

        xml.startElement('conditions', {})
        for condition_uri in optionset['conditions']:
            self.render_text_element(xml, 'condition', {'dc:uri': condition_uri}, None)
        xml.endElement('conditions')

        xml.endElement('optionset')

        for optionset_option in optionset['optionset_options']:
            self.render_option(xml, optionset_option.get('option'))

    def render_option(self, xml, option):
        xml.startElement('option', {'dc:uri': option['uri']})
        self.render_text_element(xml, 'uri_prefix', {}, option['uri_prefix'])
        self.render_text_element(xml, 'uri_path', {}, option['uri_path'])
        self.render_text_element(xml, 'dc:comment', {}, option['comment'])

        for lang_code, lang_string, lang_field in get_languages():
            self.render_text_element(xml, 'text', {'lang': lang_code}, option['text_%s' % lang_code])

        self.render_text_element(xml, 'additional_input', {}, option['additional_input'])
        xml.endElement('option')


class OptionSetRenderer(OptionsRenderer):

    def render_document(self, xml, optionsets):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'created': self.created
        })
        for optionset in optionsets:
            self.render_optionset(xml, optionset)
        xml.endElement('rdmo')


class OptionRenderer(OptionsRenderer):

    def render_document(self, xml, options):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'created': self.created
        })
        for option in options:
            self.render_option(xml, option)
        xml.endElement('rdmo')
