from rdmo.core.renderers import BaseXMLRenderer

from .mixins import ViewsRendererMixin


class ViewRenderer(ViewsRendererMixin, BaseXMLRenderer):

    def render_document(self, xml, views):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'version': self.version,
            'created': self.created
        })
        for view in views:
            self.render_view(xml, view)
        xml.endElement('rdmo')
