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


def fetch_current_values(values, current_project, snapshot=None):
    # map the values of the current project to their attribute/set_prefix/set_index/collection_index
    current_values = {
        (value.attribute_id, value.set_prefix, value.set_index, value.collection_index): value
        for value in current_project.values.filter(snapshot=snapshot).select_related('attribute', 'option')
    }

    # add the matching current value to each (unsaved) value, or None if there is no such value
    for value in values:
        if value.attribute_id is not None:
            value._current = current_values.get(
                (value.attribute_id, value.set_prefix, value.set_index, value.collection_index)
            )
