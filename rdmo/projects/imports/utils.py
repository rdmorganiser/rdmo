from django.http import Http404
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError

from rdmo.core.imports import handle_uploaded_file
from rdmo.core.plugins import get_plugin, get_plugins


def handle_import(request, plugin_key, current_project=None):
    plugin = get_plugin('PROJECT_IMPORTS', plugin_key)
    if plugin is None:
        raise Http404

    plugin.request = request
    plugin.current_project = current_project

    if request.method == 'GET':
        if not hasattr(plugin, 'render'):
            raise Http404

        return plugin.render()
    else:
        if not hasattr(plugin, 'submit'):
            raise Http404

        return plugin.submit()


def handle_upload(request, current_project=None):
    try:
        uploaded_file = request.FILES['uploaded_file']
    except KeyError as e:
        raise ValidationError({'uploaded_file': [_('This field may not be blank.')]}) from e

    file_name = handle_uploaded_file(uploaded_file)

    plugin = find_import_plugin(request, file_name, current_project)
    if plugin is None:
        raise ValidationError({'uploaded_file': [_('Files of this type cannot be imported.')]})

    if not hasattr(plugin, 'process'):
        raise Http404

    plugin.process()

    return plugin.render()


def find_import_plugin(request, file_name, current_project=None):
    for plugin in get_plugins('PROJECT_IMPORTS').values():
        plugin.request = request
        plugin.current_project = current_project
        plugin.file_name = file_name

        if hasattr(plugin, 'check') and plugin.check():
            return plugin
