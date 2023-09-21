from rdmo.conditions.renderers.mixins import ConditionRendererMixin
from rdmo.core.renderers import BaseXMLRenderer
from rdmo.domain.renderers.mixins import AttributeRendererMixin
from rdmo.options.renderers.mixins import OptionRendererMixin, OptionSetRendererMixin

from .mixins import (
    CatalogRendererMixin,
    PageRendererMixin,
    QuestionRendererMixin,
    QuestionSetRendererMixin,
    SectionRendererMixin,
)


class CatalogRenderer(CatalogRendererMixin, SectionRendererMixin, PageRendererMixin,
                      QuestionSetRendererMixin, QuestionRendererMixin, ConditionRendererMixin,
                      AttributeRendererMixin, OptionRendererMixin, OptionSetRendererMixin, BaseXMLRenderer):

    def render_document(self, xml, catalogs):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'version': self.version,
            'created': self.created
        })
        for catalog in catalogs:
            self.render_catalog(xml, catalog)
        xml.endElement('rdmo')


class SectionRenderer(SectionRendererMixin, PageRendererMixin, QuestionSetRendererMixin, QuestionRendererMixin,
                      ConditionRendererMixin, AttributeRendererMixin, OptionRendererMixin, OptionSetRendererMixin,
                      BaseXMLRenderer):

    def render_document(self, xml, sections):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'version': self.version,
            'created': self.created
        })
        for section in sections:
            self.render_section(xml, section)
        xml.endElement('rdmo')


class PageRenderer(PageRendererMixin, QuestionSetRendererMixin, QuestionRendererMixin, ConditionRendererMixin,
                   AttributeRendererMixin, OptionRendererMixin, OptionSetRendererMixin, BaseXMLRenderer):

    def render_document(self, xml, pages):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'version': self.version,
            'created': self.created
        })
        for page in pages:
            self.render_page(xml, page)
        xml.endElement('rdmo')


class QuestionSetRenderer(QuestionSetRendererMixin, QuestionRendererMixin, ConditionRendererMixin,
                          AttributeRendererMixin, OptionRendererMixin, OptionSetRendererMixin, BaseXMLRenderer):

    def render_document(self, xml, questionsets):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'version': self.version,
            'created': self.created
        })
        for questionset in questionsets:
            self.render_questionset(xml, questionset)
        xml.endElement('rdmo')


class QuestionRenderer(QuestionRendererMixin, ConditionRendererMixin, AttributeRendererMixin,
                       OptionRendererMixin, OptionSetRendererMixin, BaseXMLRenderer):

    def render_document(self, xml, questions):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'version': self.version,
            'created': self.created
        })
        for question in questions:
            self.render_question(xml, question)
        xml.endElement('rdmo')
