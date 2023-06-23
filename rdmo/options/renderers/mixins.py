from rdmo.core.utils import get_languages


class OptionSetRendererMixin:

    def render_optionset(self, xml, optionset):
        if optionset['uri'] not in self.uris:
            self.uris.add(optionset['uri'])

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
            for condition in optionset['conditions']:
                self.render_text_element(xml, 'condition', {'dc:uri': condition['uri']}, None)
            xml.endElement('conditions')

            xml.endElement('optionset')

        for optionset_option in optionset['optionset_options']:
            self.render_option(xml, optionset_option.get('option'))

        if self.context.get('conditions'):
            for condition in optionset['conditions']:
                self.render_condition(xml, condition)


class OptionRendererMixin:

    def render_option(self, xml, option):
        if option['uri'] not in self.uris:
            self.uris.add(option['uri'])

            xml.startElement('option', {'dc:uri': option['uri']})
            self.render_text_element(xml, 'uri_prefix', {}, option['uri_prefix'])
            self.render_text_element(xml, 'uri_path', {}, option['uri_path'])
            self.render_text_element(xml, 'dc:comment', {}, option['comment'])

            for lang_code, lang_string, lang_field in get_languages():
                self.render_text_element(xml, 'text', {'lang': lang_code}, option['text_%s' % lang_code])

            self.render_text_element(xml, 'additional_input', {}, option['additional_input'])
            xml.endElement('option')
