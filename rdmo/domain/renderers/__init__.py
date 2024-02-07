from rdmo.core.renderers import BaseXMLRenderer

from .mixins import AttributeRendererMixin


class AttributeRenderer(AttributeRendererMixin, BaseXMLRenderer):

    def render_document(self, xml, attributes):
        xml.startElement('rdmo', {
            'xmlns:dc': "http://purl.org/dc/elements/1.1/",
            'version': self.version,
            'created': self.created
        })
        for attribute in attributes:
            self.render_attribute(xml, attribute)
        xml.endElement('rdmo')
