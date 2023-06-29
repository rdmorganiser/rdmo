from rdmo.core.utils import get_languages


class TasksRendererMixin:

    def render_task(self, xml, task):
        if task['uri'] not in self.uris:
            self.uris.add(task['uri'])

            xml.startElement('task', {'dc:uri': task['uri']})
            self.render_text_element(xml, 'uri_prefix', {}, task['uri_prefix'])
            self.render_text_element(xml, 'uri_path', {}, task['uri_path'])
            self.render_text_element(xml, 'dc:comment', {}, task['comment'])

            for lang_code, lang_string, lang_field in get_languages():
                self.render_text_element(xml, 'title', {'lang': lang_code}, task['title_%s' % lang_code])
                self.render_text_element(xml, 'text', {'lang': lang_code}, task['text_%s' % lang_code])

            self.render_text_element(xml, 'start_attribute',  {'dc:uri': task['start_attribute']}, None)
            self.render_text_element(xml, 'end_attribute',  {'dc:uri': task['end_attribute']}, None)
            self.render_text_element(xml, 'days_before', {}, task['days_before'])
            self.render_text_element(xml, 'days_after', {}, task['days_after'])

            xml.startElement('conditions', {})
            if 'conditions' in task and task['conditions']:
                for condition in task['conditions']:
                    self.render_text_element(xml, 'condition', {'dc:uri': condition['uri']}, None)
            xml.endElement('conditions')

            xml.startElement('catalogs', {})
            if 'catalogs' in task and task['catalogs']:
                for catalog in task['catalogs']:
                    self.render_text_element(xml, 'catalog', {'dc:uri': catalog}, None)
            xml.endElement('catalogs')

            xml.endElement('task')

        if self.context.get('conditions'):
            for condition in task['conditions']:
                self.render_condition(xml, condition)
