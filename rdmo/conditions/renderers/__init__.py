from rdmo.core.renderers import BaseXMLRenderer
from rdmo.domain.renderers.mixins import AttributeRendererMixin
from rdmo.options.renderers.mixins import OptionRendererMixin

from .mixins import ConditionRendererMixin


class ConditionRenderer(ConditionRendererMixin, AttributeRendererMixin, OptionRendererMixin, BaseXMLRenderer):

    def render_document(self, xml, conditions):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'version': self.version,
            'created': self.created
        })
        for condition in conditions:
            self.render_condition(xml, condition)
        xml.endElement('rdmo')
