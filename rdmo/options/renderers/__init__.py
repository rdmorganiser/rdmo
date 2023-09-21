from rdmo.conditions.renderers.mixins import ConditionRendererMixin
from rdmo.core.renderers import BaseXMLRenderer
from rdmo.domain.renderers.mixins import AttributeRendererMixin

from .mixins import OptionRendererMixin, OptionSetRendererMixin


class OptionSetRenderer(OptionSetRendererMixin, OptionRendererMixin, ConditionRendererMixin,
                        AttributeRendererMixin, BaseXMLRenderer):

    def render_document(self, xml, optionsets):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'version': self.version,
            'created': self.created
        })
        for optionset in optionsets:
            self.render_optionset(xml, optionset)
        xml.endElement('rdmo')


class OptionRenderer(OptionRendererMixin, BaseXMLRenderer):

    def render_document(self, xml, options):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'version': self.version,
            'created': self.created
        })
        for option in options:
            self.render_option(xml, option)
        xml.endElement('rdmo')
