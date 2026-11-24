from django.http import Http404

from rdmo.core.plugins import get_plugin


def handle_export(request, plugin_key, project):
    plugin = get_plugin('PROJECT_EXPORTS', plugin_key)
    if plugin is None:
        raise Http404

    plugin.request = request
    plugin.project = project

    if request.method == 'GET':
        if not hasattr(plugin, 'render'):
            raise Http404

        return plugin.render()
    else:
        if not hasattr(plugin, 'submit'):
            raise Http404

        return plugin.submit()
