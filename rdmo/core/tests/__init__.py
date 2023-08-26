
from rdmo.core.models import Model

multisite_users = (
    ('user', 'user'),
    ('reviewer', 'reviewer'),
    ('editor', 'editor'),
    ('example-reviewer', 'example-reviewer'),
    ('example-editor', 'example-editor'),
    ('foo-user', 'foo-user'),
    ('foo-reviewer', 'foo-reviewer'),
    ('foo-editor', 'foo-editor'),
    ('bar-user', 'bar-user'),
    ('bar-reviewer', 'bar-reviewer'),
    ('bar-editor', 'bar-editor'),
    ('anonymous', None),
)


multisite_status_map = {
    'list': {
        'foo-user': 403, 'foo-reviewer': 200, 'foo-editor': 200,
        'bar-user': 403, 'bar-reviewer': 200, 'bar-editor': 200,
        'user': 403, 'example-reviewer': 200, 'example-editor': 200,
        'anonymous': 401, 'reviewer': 200, 'editor': 200,
    },
    'detail': {
        'foo-user': 404, 'foo-reviewer': 200, 'foo-editor': 200,
        'bar-user': 404, 'bar-reviewer': 200, 'bar-editor': 200,
        'user': 404, 'example-reviewer': 200, 'example-editor': 200,
        'anonymous': 401, 'reviewer': 200, 'editor': 200,
    },
    'nested': {
        'foo-user': 404, 'foo-reviewer': 200, 'foo-editor': 200,
        'bar-user': 404, 'bar-reviewer': 200, 'bar-editor': 200,
        'user': 404, 'example-reviewer': 200, 'example-editor': 200,
        'anonymous': 401, 'reviewer': 200, 'editor': 200,
    },
    'create': {
        'foo-user': 403, 'foo-reviewer': 403, 'foo-editor': 201,
        'bar-user': 403, 'bar-reviewer': 403, 'bar-editor': 201,
        'user': 403, 'example-reviewer': 403, 'example-editor': 201,
        'anonymous': 401, 'reviewer': 403, 'editor': 201,
    },
    'copy': {
        'foo-user': 404, 'foo-reviewer': 403, 'foo-editor': 201,
        'bar-user': 404, 'bar-reviewer': 403, 'bar-editor': 201,
        'user': 404, 'example-reviewer': 403, 'example-editor': 201,
        'anonymous': 401, 'reviewer': 403, 'editor': 201,
    },
    'update': {
        'foo-user': 404, 'foo-reviewer': 403, 'foo-editor': 200,
        'bar-user': 404, 'bar-reviewer': 403, 'bar-editor': 200,
        'user': 404, 'example-reviewer': 403, 'example-editor': 200,
        'anonymous': 401, 'reviewer': 403, 'editor': 200,
    },
    'delete': {
        'foo-user': 404, 'foo-reviewer': 403, 'foo-editor': 204,
        'bar-user': 404, 'bar-reviewer': 403, 'bar-editor': 204,
        'user': 404, 'example-reviewer': 403, 'example-editor': 204,
        'anonymous': 401, 'reviewer': 403, 'editor': 204,
    }
}


status_map_object_permissions = {
    'copy': {
        'all-element': {
            'foo-reviewer': 403, 'foo-editor': 201,
            'bar-reviewer': 403, 'bar-editor': 201,
            'example-reviewer': 403, 'example-editor': 201,
        },
        'foo-element': {
            'foo-reviewer': 403, 'foo-editor': 201,
            'bar-reviewer': 404, 'bar-editor': 404,
            'example-reviewer': 404, 'example-editor': 404,
        },
        'bar-element': {
            'foo-reviewer': 404, 'foo-editor': 404,
            'bar-reviewer': 403, 'bar-editor': 201,
            'example-reviewer': 404, 'example-editor': 404,
        }
    },
    'update': {
        'all-element': {
            'foo-reviewer': 403, 'foo-editor': 200,
            'bar-reviewer': 403, 'bar-editor': 200,
            'example-reviewer': 403, 'example-editor': 200,
        },
        'foo-element': {
            'foo-reviewer': 403, 'foo-editor': 200,
            'bar-reviewer': 404, 'bar-editor': 404,
            'example-reviewer': 404, 'example-editor': 404,
        },
        'bar-element': {
            'foo-reviewer': 404, 'foo-editor': 404,
            'bar-reviewer': 403, 'bar-editor': 200,
            'example-reviewer': 404, 'example-editor': 404,
        }
    },
    'delete': {
        'all-element': {
            'foo-reviewer': 403, 'foo-editor': 204,
            'bar-reviewer': 403, 'bar-editor': 204,
            'example-reviewer': 403, 'example-editor': 204,
        },
        'foo-element': {
            'foo-reviewer': 403, 'foo-editor': 204,
            'bar-reviewer': 404, 'bar-editor': 404,
            'example-reviewer': 404, 'example-editor': 404,
        },
        'bar-element': {
            'foo-reviewer': 404, 'foo-editor': 404,
            'bar-reviewer': 403, 'bar-editor': 204,
            'example-reviewer': 404, 'example-editor': 404,
        }
    },
}


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
