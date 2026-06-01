import hashlib

from django.db.models import Model

from rdmo.core.tests.constants import multisite_status_map, status_map_object_permissions


def get_obj_perms_status_code(instance, username, action, editors=None):
    ''' looks for the object permissions of the instance and returns the status code '''

    instance_uri, instance_editors = get_uri_and_editors_from_instance(instance)

    if editors is not None and action == 'delete':
        # override in case of deleted instance
        instance_editors = editors

    instance_obj_perms_key, expected_editors = get_obj_perms_key_and_expected_editors_from_uri(instance_uri)
    instance_editors = validate_or_infer_instance_editors(
        instance_uri, instance_editors, instance_obj_perms_key, expected_editors, action
    )

    if not instance_editors:
        return multisite_status_map[action][username]

    try:
        action_instance_obj_perms_map = status_map_object_permissions[action][instance_obj_perms_key]
    except KeyError as e:
        raise KeyError(
            f'instance (uri={instance_uri}, editors={instance_editors}) for {action} ({instance_obj_perms_key})'
            f' should be defined in status_map_object_permissions'
        ) from e
    try:
        return action_instance_obj_perms_map[username]
    except KeyError:
        # not all users are defined in the object-permission status map
        return multisite_status_map[action][username]


def get_uri_and_editors_from_instance(instance):
    if isinstance(instance, str):
        return instance, []

    if isinstance(instance, Model) and hasattr(instance, 'uri') and hasattr(instance, 'editors'):
        return instance.uri, instance.editors.values_list('domain', flat=True)

    raise TypeError(f'instance {instance} should be a str or a Model with uri and editors')


def get_obj_perms_key_and_expected_editors_from_uri(instance_uri):
    if 'foo-' in instance_uri:
        return 'foo-element', ['foo.com']
    if 'bar-' in instance_uri:
        return 'bar-element', ['bar.com']
    if 'example-' in instance_uri:
        return 'example-element', ['example.com']

    return 'all-element', ['foo.com', 'bar.com', 'example.com']


def validate_or_infer_instance_editors(instance_uri, instance_editors, obj_perms_key, expected_editors, action):
    if instance_editors and obj_perms_key == 'all-element':
        raise ValueError(f"uri {instance_uri} should contain the domain for {instance_editors}")

    if not instance_editors and obj_perms_key != 'all-element':
        if 'import' in action:
            # override for import when only uri is passed
            return expected_editors

        raise ValueError(f"instance_editors should be specified on {instance_uri}")

    if instance_editors:
        assert all(
            editor in instance_editors for editor in expected_editors
        ), f"{expected_editors} should be specified on {instance_uri}"

    return instance_editors


def compute_checksum(string):
    return hashlib.sha1(string).hexdigest()
