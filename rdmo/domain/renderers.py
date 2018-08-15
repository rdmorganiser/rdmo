from rdmo.core.renderers import BaseXMLRenderer


class XMLRenderer(BaseXMLRenderer):

    def render_document(self, xml, attribute_entities):
        xml.startElement('domain', {
            'xmlns:dc': "http://purl.org/dc/elements/1.1/"
        })

        for attribute_entity in attribute_entities:
            if attribute_entity['is_attribute']:
                self.render_attribute(xml, attribute_entity)
            else:
                self.render_attribute_entity(xml, attribute_entity)

        xml.endElement('domain')

    def render_attribute_entity(self, xml, attribute_entity):
        xml.startElement('entity', {})
        self.render_text_element(xml, 'dc:uri', {}, attribute_entity["uri"])
        self.render_text_element(xml, 'dc:comment', {}, attribute_entity["comment"])

        if 'children' in attribute_entity:
            xml.startElement('children', {})
            for child in attribute_entity['children']:
                if child['is_attribute']:
                    self.render_attribute(xml, child)
                else:
                    self.render_attribute_entity(xml, child)
            xml.endElement('children')

        xml.endElement('entity')

    def render_attribute(self, xml, attribute):
        xml.startElement('attribute', {})
        self.render_text_element(xml, 'dc:uri', {}, attribute["uri"])
        self.render_text_element(xml, 'dc:comment', {}, attribute["comment"])
        xml.endElement('attribute')
