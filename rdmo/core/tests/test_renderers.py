from ..renderers import BaseXMLRenderer


class TestRenderer(BaseXMLRenderer):

    def render_document(self, xml, data):
        xml.startElement('rdmo', {
            'xmlns:dc': "http://purl.org/dc/elements/1.1/",
            'version': self.version,
            'created': self.created
        })
        self.render_text_element(xml, 'text', {}, data['text'])
        xml.endElement('rdmo')


def test_render():
    renderer = TestRenderer()
    xml = renderer.render({'text': 'test'})
    assert '<text>test</text>' in xml


def test_render_ascii_code():
    renderer = TestRenderer()
    xml = renderer.render({'text': 'te' + b'\x02'.decode() + 'st'})
    assert '<text>test</text>' in xml
