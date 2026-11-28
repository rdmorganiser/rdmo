import pytest

from django.urls import reverse

users = (
    'owner',
    'manager',
    'author',
    'guest',
    'admin',
    'api',
    'site',
    'user',
    'anonymous',
)

export_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10, 12],
    'manager': [1, 3, 5, 7],
    'admin': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
}

projects = [1, 2, 3, 4, 5, 12]

plugin_keys = [
    'xml',
    'set',
]

plugin_download = [
    'xml',
]

urlnames = {
    'export': 'v1-projects:project-export',
}

@pytest.mark.parametrize('username', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('plugin_key', plugin_keys)
def test_get(db, client, login, username, project_id, plugin_key):
    login(username)

    url = reverse(urlnames['export'], args=[project_id, plugin_key])
    response = client.get(url)

    if username == 'anonymous':
        assert response.status_code == 401
    elif project_id in export_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert response['content-type'] == 'application/xml' if plugin_key in plugin_download else 'application/json'
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('plugin_key', plugin_keys)
def test_post(db, client, login, username, project_id, plugin_key):
    login(username)

    url = reverse(urlnames['export'], args=[project_id, plugin_key])
    response = client.post(url)

    if username == 'anonymous':
        assert response.status_code == 401
    elif project_id in export_project_permission_map.get(username, []):
        assert response.status_code == 404 if plugin_key in plugin_download else 200
    else:
        assert response.status_code == 404
