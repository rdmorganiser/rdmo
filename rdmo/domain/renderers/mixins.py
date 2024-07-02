class AttributeRendererMixin:

    def render_attribute(self, xml, attribute, include_children=True):
        if attribute['uri'] not in self.uris:
            self.uris.add(attribute['uri'])

            xml.startElement('attribute', {'dc:uri': attribute['uri']})
            self.render_text_element(xml, 'uri_prefix', {}, attribute['uri_prefix'])
            self.render_text_element(xml, 'key', {}, attribute['key'])
            self.render_text_element(xml, 'path', {}, attribute['path'])
            self.render_text_element(xml, 'dc:comment', {}, attribute['comment'])
            self.render_text_element(xml, 'parent', {'dc:uri': attribute['parent']}, None)
            xml.endElement('attribute')

        if include_children:
            for child in attribute.get('children', []):
                self.render_attribute(xml, child)

        parent_data = attribute.get('parent_data')
        if parent_data:
            self.render_attribute(xml, parent_data, include_children=False)
