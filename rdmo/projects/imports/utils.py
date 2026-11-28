from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError

from rdmo.core.imports import handle_uploaded_file
from rdmo.core.plugins import get_plugin, get_plugins
from rdmo.questions.models import Catalog

from ..models import Membership, Project


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

    if not hasattr(plugin, 'render'):
        raise Http404

    return plugin.render()


def find_import_plugin(request, file_name, current_project=None):
    for plugin in get_plugins('PROJECT_IMPORTS').values():
        plugin.request = request
        plugin.current_project = current_project
        plugin.file_name = file_name

        if plugin.upload and plugin.check():
            return plugin


def get_imports():
    return {
        key: {
            'label': plugin.label,
            'description': plugin.description,
            'upload': plugin.upload,
            'accept': plugin.accept
        }
        for key, plugin in get_plugins('PROJECT_IMPORTS').items()
    }


def fetch_current_project(project, current_project):
    if current_project is None:
        return

    # add the current project to the (unsaved) project, and the current values to its values
    project._current = current_project
    fetch_current_values(project._values, current_project)
    fetch_current_snapshots(project._snapshots, current_project)


def fetch_current_snapshots(snapshots, current_project):
    # match the snapshots by their index, the export uses the default ordering of the snapshots as well
    current_snapshots = list(current_project.snapshots.all())

    # add the matching current snapshot to each (unsaved) snapshot, or None if there is no such snapshot,
    # and the current values of this snapshot to its values
    for snapshot in snapshots:
        if snapshot._index < len(current_snapshots):
            current_snapshot = current_snapshots[snapshot._index]
            snapshot._current = current_snapshot
            fetch_current_values(snapshot._values, current_project, snapshot=current_snapshot)
        else:
            snapshot._current = None


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


@transaction.atomic
def create_project(request, title, description='', catalog_uri=None):
    available_catalogs = Catalog.objects.filter_for_user(request.user)
    catalog = available_catalogs.filter(uri=catalog_uri).first() or available_catalogs.first()

    project = Project.objects.create(
        title=title,
        description=description,
        catalog=catalog,
        site=get_current_site(request)
    )

    # add the current user as owner
    Membership.objects.create(project=project, user=request.user, role='owner')

    return project


@transaction.atomic
def save_project(import_project, current_project=None):
    if import_project.pk is not None:
        raise RuntimeError(f'Imported project {import_project.pk} is already saved.')

    if current_project is None:
        project = import_project
    else:
        project = current_project
        project.title = import_project.title
        project.description = import_project.description
        project.catalog = import_project.catalog

    # save the project
    project.save()

    # import the values
    for value in getattr(import_project, '_values', []):
        save_value(value, project)

    # import the snapshots and their values
    for snapshot in getattr(import_project, '_snapshots', []):
        save_snapshot(snapshot, project)


@transaction.atomic
def save_snapshot(import_snapshot, project):
    if import_snapshot.pk is not None:
        raise RuntimeError(f'Imported snapshot {import_snapshot.pk} is already saved.')

    current_snapshot = getattr(import_snapshot, '_current', None)

    if current_snapshot is None:
        snapshot = import_snapshot
        snapshot.project = project
    else:
        if current_snapshot.pk is None or current_snapshot.project_id != project.id:
            raise RuntimeError(f'Current snapshot {current_snapshot.pk} does not match the imported snapshot.')

        snapshot = current_snapshot
        snapshot.title = import_snapshot.title
        snapshot.description = import_snapshot.description

    # save the snapshot, but do not copy the current values of the project
    snapshot.save(copy_values=False)

    # import the values
    for value in getattr(import_snapshot, '_values', []):
        save_value(value, project, snapshot)


def save_value(import_value, project, snapshot=None):
    if import_value.pk is not None:
        raise RuntimeError(f'Imported value {import_value.pk} is already saved.')

    if import_value.attribute is None:
        return  # skip values for attributes, which are not in the database

    current_value = getattr(import_value, '_current', None)

    if current_value is None:
        value = import_value
        value.project = project
        value.snapshot = snapshot
    else:
        if (
            current_value.pk is None
            or current_value.project_id != project.id
            or current_value.snapshot_id != (snapshot.id if snapshot else None)
            or current_value.attribute_id != import_value.attribute_id
            or current_value.set_prefix != import_value.set_prefix
            or current_value.set_index != import_value.set_index
            or current_value.collection_index != import_value.collection_index
        ):
            raise RuntimeError(f'Current value {current_value.pk} does not match the imported value.')

        value = current_value
        value.set_collection = import_value.set_collection
        value.text = import_value.text
        value.option = import_value.option
        value.external_id = import_value.external_id
        value.value_type = import_value.value_type
        value.unit = import_value.unit

    # save the value
    value.save()

    # import the file, note that the file operations are not part of the database transaction
    # of save_project or save_snapshot: if the import fails, deleted files are not restored
    # and new files are not removed
    if import_value.file:
        if current_value is not None:
            value.file.delete()
        value.copy_file(import_value.file_name, import_value.file)
    else:
        try:
            name = import_value.file_import.get('name')
            file = import_value.file_import.get('file')
            if current_value is not None:
                value.file.delete()
            value.file.save(name, file)
        except AttributeError:
            pass
