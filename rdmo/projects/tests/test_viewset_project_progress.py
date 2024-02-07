import pytest

from django.urls import reverse

from ..models import Project

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('api', 'api'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

view_progress_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10],
    'manager': [1, 3, 5, 7],
    'author': [1, 3, 5, 8],
    'guest': [1, 3, 5, 9],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
}

change_progress_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10],
    'manager': [1, 3, 5, 7],
    'author': [1, 3, 5, 8],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
}

urlnames = {
    'progress': 'v1-projects:project-progress'
}

projects = [1, 2, 3, 4, 5]

@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_progress_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['progress'], args=[project_id])
    response = client.get(url)

    if project_id in view_progress_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

        project = Project.objects.get(id=project_id)
        assert response.json()['count'] == project.progress_count
        assert response.json()['total'] == project.progress_total

    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_progress_post(db, client, username, password, project_id):
    client.login(username=username, password=password)

    if project_id in change_progress_permission_map.get(username, []):
        # set project count and value to a different value
        project = Project.objects.get(id=project_id)
        project.progress_count = 0
        project.progress_total = 0
        project.save()

    url = reverse(urlnames['progress'], args=[project_id])
    response = client.post(url)

    if project_id in change_progress_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

        project.refresh_from_db()
        assert response.json()['count'] > 0
        assert response.json()['total'] > 0

    else:
        if project_id in view_progress_permission_map.get(username, []):
            assert response.status_code == 403
        elif password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401
