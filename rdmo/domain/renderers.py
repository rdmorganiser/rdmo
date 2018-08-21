from rdmo.core.renderers import BaseXMLRenderer


class XMLRenderer(BaseXMLRenderer):

    def render_document(self, xml, attributes):
        xml.startElement('domain', {
            'xmlns:dc': "http://purl.org/dc/elements/1.1/"
        })

        for attribute in attributes:
                self.render_attribute(xml, attribute)

        xml.endElement('domain')

    def render_attribute(self, xml, attribute):
        xml.startElement('attribute', {})
        self.render_text_element(xml, 'dc:uri', {}, attribute["uri"])
        self.render_text_element(xml, 'dc:comment', {}, attribute["comment"])

        if 'children' in attribute:
            xml.startElement('children', {})
            for child in attribute['children']:
                    self.render_attribute(xml, child)
            xml.endElement('children')

        xml.endElement('attribute')
