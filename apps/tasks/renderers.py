from apps.core.renderers import BaseXMLRenderer


class XMLRenderer(BaseXMLRenderer):

    def render_document(self, xml, tasks):
        xml.startElement('tasks', {
            'xmlns:dc': "http://purl.org/dc/elements/1.1/"
        })

        for task in tasks:
            self.render_task(xml, task)

        xml.endElement('tasks')

    def render_task(self, xml, task):
        xml.startElement('task', {})
        self.render_text_element(xml, 'dc:uri', {}, task["uri"])
        self.render_text_element(xml, 'dc:comment', {}, task["comment"])
        self.render_text_element(xml, 'attribute', {'dc:uri': task["attribute"]}, None)
        self.render_text_element(xml, 'time_period', {}, task["time_period"])
        self.render_text_element(xml, 'title', {'lang': 'en'}, task["title_en"])
        self.render_text_element(xml, 'title', {'lang': 'de'}, task["title_de"])
        self.render_text_element(xml, 'text', {'lang': 'en'}, task["text_en"])
        self.render_text_element(xml, 'text', {'lang': 'de'}, task["text_de"])
        xml.startElement('conditions', {})
        for condition in task["conditions"]:
            self.render_text_element(xml, 'condition', {'dc:uri': condition}, None)
        xml.endElement('conditions')
        xml.endElement('task')

