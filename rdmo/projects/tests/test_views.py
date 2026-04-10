import pytest

from django.urls import reverse

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('api', 'api'),
    ('site', 'site'),
    ('anonymous', None)
)

view_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10, 12],
    'manager': [1, 3, 5, 7, 12],
    'author': [1, 3, 5, 8, 12],
    'guest': [1, 3, 5, 9, 12],
    'user': [12],
    'editor': [12],
    'reviewer': [12],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
}

projects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('projects')
    response = client.get(url)

    if password:
        assert response.status_code == 200
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_detail(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project', args=[project_id])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_error(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_error', args=[project_id])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
