import pytest
from django.urls import reverse

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

view_questionset_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'guest': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

urlnames = {
    'list': 'v1-projects:project-questionset-list',
    'detail': 'v1-projects:project-questionset-detail'
}

projects = [1, 2, 3, 4, 5]
questionsets = [1]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('questionset_id', questionsets)
def test_detail(db, client, username, password, project_id, questionset_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[project_id, questionset_id])
    response = client.get(url)

    if project_id in view_questionset_permission_map.get(username, []):
        assert response.status_code == 200
        assert response.json().get('id') == questionset_id
    else:
        assert response.status_code == 404
