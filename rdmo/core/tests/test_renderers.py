from django.conf import settings

from rdmo import __version__

from ..renderers import BaseXMLRenderer


class TestRenderer(BaseXMLRenderer):

    def render_document(self, xml, data):
        xml.startElement('rdmo', {
            'xmlns:dc': "http://purl.org/dc/elements/1.1/",
            'version': self.version,
            'required': self.required,
            'created': self.created
        })
        self.render_text_element(xml, 'text', {}, data['text'])
        xml.endElement('rdmo')


def test_render():
    renderer = TestRenderer()
    xml = renderer.render({'text': 'test'})
    assert '<text>test</text>' in xml
    assert f'version="{__version__}"' in xml
    assert f'required="{settings.EXPORT_MIN_REQUIRED_VERSION}"' in xml


def test_render_ascii_code():
    renderer = TestRenderer()
    xml = renderer.render({'text': 'te' + b'\x02'.decode() + 'st'})
    assert '<text>test</text>' in xml
