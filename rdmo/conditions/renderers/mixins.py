class ConditionRendererMixin:

    def render_condition(self, xml, condition):
        if condition['uri'] not in self.uris:
            self.uris.add(condition['uri'])

            xml.startElement('condition', {'dc:uri': condition['uri']})
            self.render_text_element(xml, 'uri_prefix', {}, condition['uri_prefix'])
            self.render_text_element(xml, 'uri_path', {}, condition['uri_path'])
            self.render_text_element(xml, 'dc:comment', {}, condition['comment'])
            self.render_text_element(xml, 'source', {'dc:uri': condition['source']['uri']}, None)
            self.render_text_element(xml, 'relation', {}, condition['relation'])
            self.render_text_element(xml, 'target_text', {}, condition['target_text'])
            self.render_text_element(xml, 'target_option', {
                'dc:uri': condition['target_option']['uri'] if condition['target_option'] is not None else None
            }, None)
            xml.endElement('condition')

        if self.context.get('attributes'):
            self.render_attribute(xml, condition['source'])

        if self.context.get('options'):
            if condition['target_option'] is not None:
                self.render_option(xml, condition['target_option'])
