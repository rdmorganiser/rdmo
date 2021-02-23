import pytest
from django.urls import reverse

from ..models import Issue

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

view_issue_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'guest': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

add_issue_permission_map = delete_issue_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

change_issue_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

urlnames = {
    'list': 'v1-projects:project-issue-list',
    'detail': 'v1-projects:project-issue-detail'
}

projects = [1, 2, 3, 4, 5]
issues = [1, 2, 3, 4]

issue_status = ('open', 'in_progress', 'closed')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_list(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    response = client.get(url)

    if project_id in view_issue_permission_map.get(username, []):
        assert response.status_code == 200

        if username == 'user':
            assert sorted([item['id'] for item in response.json()]) == []
        else:
            values_list = Issue.objects.filter(project_id=project_id) \
                                       .order_by('id').values_list('id', flat=True)
            assert sorted([item['id'] for item in response.json()]) == list(values_list)
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('issue_id', issues)
def test_detail(db, client, username, password, project_id, issue_id):
    client.login(username=username, password=password)
    issue = Issue.objects.filter(project_id=project_id, id=issue_id).first()

    url = reverse(urlnames['detail'], args=[project_id, issue_id])
    response = client.get(url)

    if issue and project_id in view_issue_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') == issue_id
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_create(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    response = client.post(url)

    if project_id in add_issue_permission_map.get(username, []):
        assert response.status_code == 405
    elif project_id in view_issue_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('issue_id', issues)
@pytest.mark.parametrize('status', issue_status)
def test_update(db, client, username, password, project_id, issue_id, status):
    client.login(username=username, password=password)
    issue = Issue.objects.filter(project_id=project_id, id=issue_id).first()

    url = reverse(urlnames['detail'], args=[project_id, issue_id])
    data = {
        'status': status
    }
    response = client.put(url, data, content_type='application/json')

    if issue and project_id in change_issue_permission_map.get(username, []):
        assert response.status_code == 200
        assert response.json().get('status') == status
    elif issue and project_id in view_issue_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('issue_id', issues)
def test_delete(db, client, username, password, project_id, issue_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[project_id, issue_id])
    response = client.delete(url)

    if project_id in delete_issue_permission_map.get(username, []):
        assert response.status_code == 405
    elif project_id in view_issue_permission_map.get(username, []):
        assert response.status_code == 405
    else:
        assert response.status_code == 404
