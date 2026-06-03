multisite_status_map = {
    'list': {
        'foo-user': 403, 'foo-reviewer': 403, 'foo-editor': 403,
        'bar-user': 403, 'bar-reviewer': 403, 'bar-editor': 403,
        'user': 403, 'example-reviewer': 200, 'example-editor': 200,
        'anonymous': 401, 'reviewer': 200, 'editor': 200,
    },
    'detail': {
        'foo-user': 404, 'foo-reviewer': 404, 'foo-editor': 404,
        'bar-user': 404, 'bar-reviewer': 404, 'bar-editor': 404,
        'user': 404, 'example-reviewer': 200, 'example-editor': 200,
        'anonymous': 401, 'reviewer': 200, 'editor': 200,
    },
    'nested': {
        'foo-user': 404, 'foo-reviewer': 404, 'foo-editor': 404,
        'bar-user': 404, 'bar-reviewer': 404, 'bar-editor': 404,
        'user': 404, 'example-reviewer': 200, 'example-editor': 200,
        'anonymous': 401, 'reviewer': 200, 'editor': 200,
    },
    'create': {
        'foo-user': 403, 'foo-reviewer': 403, 'foo-editor': 403,
        'bar-user': 403, 'bar-reviewer': 403, 'bar-editor': 403,
        'user': 403, 'example-reviewer': 403, 'example-editor': 201,
        'anonymous': 401, 'reviewer': 403, 'editor': 201,
    },
    'create-with-parent': {
        'foo-user': 403, 'foo-reviewer': 403, 'foo-editor': 403,
        'bar-user': 403, 'bar-reviewer': 403, 'bar-editor': 403,
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
        'foo-user': 404, 'foo-reviewer': 404, 'foo-editor': 404,
        'bar-user': 404, 'bar-reviewer': 404, 'bar-editor': 404,
        'user': 404, 'example-reviewer': 403, 'example-editor': 200,
        'anonymous': 401, 'reviewer': 403, 'editor': 200,
    },
    'delete': {
        'foo-user': 404, 'foo-reviewer': 404, 'foo-editor': 404,
        'bar-user': 404, 'bar-reviewer': 404, 'bar-editor': 404,
        'user': 404, 'example-reviewer': 403, 'example-editor': 204,
        'anonymous': 401, 'reviewer': 403, 'editor': 204,
    },
    'toggle-site': {
        # foo-editor is not permitted to apply own site(foo.com) in test run(example.com)
        'foo-user': 403, 'foo-reviewer': 403, 'foo-editor': 403,
        # bar-editor is not permitted to apply own site(bar.com) in test run(example.com)
        'bar-user': 403, 'bar-reviewer': 403, 'bar-editor': 403,
        'user': 403, 'example-reviewer': 403, 'example-editor': 200,
        'anonymous': 401, 'reviewer': 403, 'editor': 200,
    },
    'management': { # access to the ui for example.com
        'foo-user': 403, 'foo-reviewer': 403, 'foo-editor': 403,
        'bar-user': 403, 'bar-reviewer': 403, 'bar-editor': 403,
        'user': 403, 'example-reviewer': 200, 'example-editor': 200,
        'anonymous': 302, 'reviewer': 200, 'editor': 200,
    },
    'upload-import': {  # access to the ui for example.com
        'foo-user': 403, 'foo-reviewer': 403, 'foo-editor': 403,
        'bar-user': 403, 'bar-reviewer': 403, 'bar-editor': 403,
        'user': 403, 'example-reviewer': 403, 'example-editor': 200,
        'anonymous': 401, 'reviewer': 403, 'editor': 200,
    },

}
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
