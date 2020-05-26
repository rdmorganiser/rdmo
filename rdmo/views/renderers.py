from rdmo.core.renderers import BaseXMLRenderer
from rdmo.core.utils import get_languages


class XMLRenderer(BaseXMLRenderer):

    def render_document(self, xml, views):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/'
        })
        for view in views:
            self.render_view(xml, view)
        xml.endElement('rdmo')

    def render_view(self, xml, view):
        xml.startElement('view', {'dc:uri': view['uri']})
        self.render_text_element(xml, 'uri_prefix', {}, view['uri_prefix'])
        self.render_text_element(xml, 'key', {}, view['key'])
        self.render_text_element(xml, 'dc:comment', {}, view['comment'])

        for lang_code, lang_string, lang_field in get_languages():
            self.render_text_element(xml, 'title', {'lang': lang_code}, view['title_%s' % lang_code])
            self.render_text_element(xml, 'help', {'lang': lang_code}, view['help_%s' % lang_code])

        for catalog in view['catalogs']:
            xml.startElement('catalogs', {})
            self.render_text_element(xml, 'catalog', {'dc:uri': catalog}, None)
            xml.endElement('catalogs')

        self.render_text_element(xml, 'template', {}, view['template'])
        xml.endElement('view')
