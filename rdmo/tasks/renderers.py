from rdmo.core.renderers import BaseXMLRenderer


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
        self.render_text_element(xml, 'title', {'lang': 'en'}, task["title_en"])
        self.render_text_element(xml, 'title', {'lang': 'de'}, task["title_de"])
        self.render_text_element(xml, 'text', {'lang': 'en'}, task["text_en"])
        self.render_text_element(xml, 'text', {'lang': 'de'}, task["text_de"])

        xml.startElement('conditions', {})
        for condition in task["conditions"]:
            self.render_text_element(xml, 'condition', {'dc:uri': condition}, None)
        xml.endElement('conditions')

        self.render_timeframe(xml, task['timeframe'])

        xml.endElement('task')

    def render_timeframe(self, xml, timeframe):
        xml.startElement('timeframe', {})
        if timeframe:
            self.render_text_element(xml, 'start_attribute',  {'dc:uri': timeframe["start_attribute"]}, None)
            self.render_text_element(xml, 'end_attribute',  {'dc:uri': timeframe["end_attribute"]}, None)
            self.render_text_element(xml, 'days_before', {}, timeframe["days_before"])
            self.render_text_element(xml, 'days_after', {}, timeframe["days_after"])
        xml.endElement('timeframe')
