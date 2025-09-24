import hashlib

from django.db.models import Model

from rdmo.core.tests.constants import multisite_status_map, status_map_object_permissions


def get_obj_perms_status_code(instance, username, method, editors=None):
    ''' looks for the object permissions of the instance and returns the status code '''

    if (isinstance(instance, Model) or hasattr(instance, 'editors')) and hasattr(instance, 'uri'):
        instance_uri = instance.uri
        instance_editors = instance.editors.values_list('domain', flat=True)
    elif isinstance(instance, str):
        instance_uri = instance
        instance_editors = []
    else:
        raise TypeError(f'instance {instance} should be a str or a Model (and have an uri)')

    if editors is not None and method == 'delete':
        # override in case of deleted instance
        instance_editors = editors

    if 'foo-' in instance_uri:
        instance_obj_perms_key = 'foo-element'
        assert_editors = ['foo.com']
    elif 'bar-' in instance_uri:
        instance_obj_perms_key = 'bar-element'
        assert_editors = ['bar.com']
    elif 'example-' in instance_uri:
        instance_obj_perms_key = 'example-element'
        assert_editors = ['example.com']
    else:
        if instance_editors:
            raise ValueError(f"uri {instance_uri} should contain the domain for {instance_editors}")
        instance_obj_perms_key = 'all-element'
        assert_editors = ['foo.com', 'bar.com', 'example.com']

    if not instance_editors and instance_obj_perms_key != 'all-element':
        if 'import' in method:  # override for import when only uri is passed
            instance_editors = assert_editors
        else:
            raise ValueError(f"instance_editors should be specified on {instance_uri}")
    elif instance_editors:
        assert all(
            i in instance_editors for i in assert_editors
        ), f"{assert_editors} should be specified on {instance_uri}"


    if not instance_editors:
        return multisite_status_map[method][username]

    try:
        method_instance_obj_perms_map = status_map_object_permissions[method][instance_obj_perms_key]
    except KeyError as e:
        raise KeyError(
            f'instance (uri={instance_uri}, editors={instance_editors}) for {method} ({instance_obj_perms_key})'
            f' should be defined in status_map_object_permissions'
        ) from e
    try:
        return method_instance_obj_perms_map[username]
    except KeyError:
        # not all users are defined in the method_instance_perms_map
        return multisite_status_map[method][username]


def compute_checksum(string):
    return hashlib.sha1(string).hexdigest()
