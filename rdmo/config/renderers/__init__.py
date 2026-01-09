from rdmo.core.renderers import BaseXMLRenderer

from .mixins import PluginRendererMixin


class PluginRenderer(PluginRendererMixin, BaseXMLRenderer):

    def render_document(self, xml, plugins):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'version': self.version,
            'required': self.required,
            'created': self.created
        })
        for plugin in plugins:
            self.render_plugin(xml, plugin)
        xml.endElement('rdmo')


__all__ = ['PluginRenderer', 'PluginRendererMixin']
