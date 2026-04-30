import json

from rdmo.core.utils import get_languages


class PluginRendererMixin:

    def render_plugin(self, xml, plugin):
        if plugin['uri'] not in self.uris:
            self.uris.add(plugin['uri'])

            xml.startElement('plugin', {'dc:uri': plugin['uri']})
            self.render_text_element(xml, 'uri_prefix', {}, plugin['uri_prefix'])
            self.render_text_element(xml, 'uri_path', {}, plugin['uri_path'])
            self.render_text_element(xml, 'dc:comment', {}, plugin['comment'])

            for lang_code, _lang_string, _lang_field in get_languages():
                self.render_text_element(xml, 'title', {'lang': lang_code}, plugin[f'title_{lang_code}'])
                self.render_text_element(xml, 'help', {'lang': lang_code}, plugin[f'help_{lang_code}'])

            self.render_text_element(xml, 'python_path', {}, plugin['python_path'])

            plugin_settings = plugin.get('plugin_settings')
            if isinstance(plugin_settings, (dict, list)):
                plugin_settings = json.dumps(plugin_settings)
            self.render_text_element(xml, 'plugin_settings', {}, plugin_settings)

            self.render_text_element(xml, 'locked', {}, plugin['locked'])
            self.render_text_element(xml, 'order', {}, plugin['order'])
            self.render_text_element(xml, 'url_name', {}, plugin['url_name'])
            xml.endElement('plugin')
