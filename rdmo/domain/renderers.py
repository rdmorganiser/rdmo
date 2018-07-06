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
        self.render_text_element(xml, 'is_collection', {}, attribute_entity["is_collection"])
        self.render_verbosename(xml, attribute_entity['verbosename'])

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
        self.render_text_element(xml, 'is_collection', {}, attribute["is_collection"])
        self.render_range(xml, attribute['range'])
        self.render_verbosename(xml, attribute['verbosename'])
        xml.endElement('attribute')

    def render_range(self, xml, range):
        xml.startElement('range', {})
        if range:
            self.render_text_element(xml, 'minimum', {}, range["minimum"])
            self.render_text_element(xml, 'maximum', {}, range["maximum"])
            self.render_text_element(xml, 'step', {}, range["step"])
        xml.endElement('range')

    def render_verbosename(self, xml, verbosename):
        xml.startElement('verbosename', {})
        if verbosename:
            self.render_text_element(xml, 'name', {'lang': 'en'}, verbosename["name_en"])
            self.render_text_element(xml, 'name', {'lang': 'de'}, verbosename["name_de"])
            self.render_text_element(xml, 'name_plural', {'lang': 'en'}, verbosename["name_plural_en"])
            self.render_text_element(xml, 'name_plural', {'lang': 'de'}, verbosename["name_plural_de"])
        xml.endElement('verbosename')
