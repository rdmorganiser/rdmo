import hashlib

from rdmo.core.models import Model
from rdmo.core.tests.constants import multisite_status_map, status_map_object_permissions


def get_obj_perms_status_code(instance, username, method):
    ''' looks for the object permissions of the instance and returns the status code '''

    if isinstance(instance, Model):
        try:
            if not instance.editors.exists():
                return multisite_status_map[method][username]
        except AttributeError as e:
            raise AttributeError(f'instance {instance} should have an editors attribute') from e
    elif isinstance(instance, str):
        pass

    if 'foo-' in str(instance):
        instance_obj_perms_key = 'foo-element'
    elif 'bar-' in str(instance):
        instance_obj_perms_key = 'bar-element'
    else:
        instance_obj_perms_key = 'all-element'

    try:
        method_instance_obj_perms_map = status_map_object_permissions[method][instance_obj_perms_key]
    except KeyError as e:
        raise KeyError(f'instance ({instance_obj_perms_key}) should be defined in status_map_object_permissions') from e
    try:
        return method_instance_obj_perms_map[username]
    except KeyError:
        # not all users are defined in the method_instance_perms_map
        return multisite_status_map[method][username]


def compute_checksum(string):
    return hashlib.sha1(string).hexdigest()
