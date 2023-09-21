from rdmo.core.utils import get_languages


class ViewsRendererMixin:

    def render_view(self, xml, view):
        if view['uri'] not in self.uris:
            self.uris.add(view['uri'])

            xml.startElement('view', {'dc:uri': view['uri']})
            self.render_text_element(xml, 'uri_prefix', {}, view['uri_prefix'])
            self.render_text_element(xml, 'uri_path', {}, view['uri_path'])
            self.render_text_element(xml, 'dc:comment', {}, view['comment'])

            for lang_code, lang_string, lang_field in get_languages():
                self.render_text_element(xml, 'title', {'lang': lang_code}, view['title_%s' % lang_code])
                self.render_text_element(xml, 'help', {'lang': lang_code}, view['help_%s' % lang_code])

            xml.startElement('catalogs', {})
            if 'catalogs' in view and view['catalogs']:
                for catalog in view['catalogs']:
                    self.render_text_element(xml, 'catalog', {'dc:uri': catalog}, None)
            xml.endElement('catalogs')

            self.render_text_element(xml, 'template', {}, view['template'])
            xml.endElement('view')
