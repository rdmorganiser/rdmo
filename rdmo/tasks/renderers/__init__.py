from rdmo.conditions.renderers.mixins import ConditionRendererMixin
from rdmo.core.renderers import BaseXMLRenderer
from rdmo.domain.renderers.mixins import AttributeRendererMixin
from rdmo.options.renderers.mixins import OptionRendererMixin

from .mixins import TasksRendererMixin


class TaskRenderer(TasksRendererMixin, ConditionRendererMixin, AttributeRendererMixin,
                   OptionRendererMixin, BaseXMLRenderer):

    def render_document(self, xml, tasks):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'version': self.version,
            'created': self.created
        })
        for task in tasks:
            self.render_task(xml, task)
        xml.endElement('rdmo')
