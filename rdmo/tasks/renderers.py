from rdmo.core.renderers import BaseXMLRenderer


class XMLRenderer(BaseXMLRenderer):

    def render_document(self, xml, tasks):
        xml.startElement('rdmo', {
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/'
        })
        for task in tasks:
            self.render_task(xml, task)
        xml.endElement('rdmo')

    def render_task(self, xml, task):
        xml.startElement('task', {'dc:uri': task['uri']})
        self.render_text_element(xml, 'uri_prefix', {}, task['uri_prefix'])
        self.render_text_element(xml, 'key', {}, task['key'])
        self.render_text_element(xml, 'dc:comment', {}, task['comment'])
        self.render_text_element(xml, 'title', {'lang': 'en'}, task['title_en'])
        self.render_text_element(xml, 'title', {'lang': 'de'}, task['title_de'])
        self.render_text_element(xml, 'text', {'lang': 'en'}, task['text_en'])
        self.render_text_element(xml, 'text', {'lang': 'de'}, task['text_de'])
        self.render_text_element(xml, 'start_attribute',  {'dc:uri': task['start_attribute']}, None)
        self.render_text_element(xml, 'end_attribute',  {'dc:uri': task['end_attribute']}, None)
        self.render_text_element(xml, 'days_before', {}, task['days_before'])
        self.render_text_element(xml, 'days_after', {}, task['days_after'])

        xml.startElement('conditions', {})
        if 'conditions' in task and task['conditions']:
            for condition in task['conditions']:
                self.render_text_element(xml, 'condition', {'dc:uri': condition}, None)
        xml.endElement('conditions')

        xml.endElement('task')
