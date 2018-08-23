from rdmo.core.renderers import BaseXMLRenderer


class XMLRenderer(BaseXMLRenderer):

    def render_document(self, xml, conditions):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/'
        })
        for condition in conditions:
            self.render_condition(xml, condition)
        xml.endElement('rdmo')

    def render_condition(self, xml, condition):
        xml.startElement('condition', {'dc:uri': condition['uri']})
        self.render_text_element(xml, 'uri_prefix', {}, condition['uri_prefix'])
        self.render_text_element(xml, 'key', {}, condition['key'])
        self.render_text_element(xml, 'dc:comment', {}, condition['comment'])
        self.render_text_element(xml, 'source', {'dc:uri': condition['source']}, None)
        self.render_text_element(xml, 'relation', {}, condition['relation'])
        self.render_text_element(xml, 'target_text', {}, condition['target_text'])
        self.render_text_element(xml, 'target_option', {'dc:uri': condition['target_option']}, None)
        xml.endElement('condition')
