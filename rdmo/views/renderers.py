from rdmo.core.renderers import BaseXMLRenderer


class XMLRenderer(BaseXMLRenderer):

    def render_document(self, xml, views):
        xml.startElement('views', {
            'xmlns:dc': "http://purl.org/dc/elements/1.1/"
        })

        for view in views:
            self.render_view(xml, view)

        xml.endElement('views')

    def render_view(self, xml, view):
        xml.startElement('view', {})
        self.render_text_element(xml, 'dc:uri', {}, view["uri"])
        self.render_text_element(xml, 'dc:comment', {}, view["comment"])
        self.render_text_element(xml, 'title', {'lang': 'en'}, view["title_en"])
        self.render_text_element(xml, 'title', {'lang': 'de'}, view["title_de"])
        self.render_text_element(xml, 'help', {'lang': 'en'}, view["help_en"])
        self.render_text_element(xml, 'help', {'lang': 'de'}, view["help_de"])
        self.render_text_element(xml, 'template', {}, view["template"])
        xml.endElement('view')
