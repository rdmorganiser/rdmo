import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Invite

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

view_invite_permission_map = {
    'owner': [1],
    'manager': [],
    'author': [],
    'guest': [],
    'api': [1, 11],
    'site': [1, 11]
}

add_invite_permission_map = change_invite_permission_map = delete_invite_permission_map = {
    'owner': [1],
    'api': [1, 11],
    'site': [1, 11]
}

urlnames = {
    'list': 'v1-projects:project-invite-list',
    'detail': 'v1-projects:project-invite-detail'
}

projects = [1, 11]
invites = [1, 2]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_list(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    response = client.get(url)

    if project_id in view_invite_permission_map.get(username, []):
        assert response.status_code == 200

        if username == 'user':
            assert sorted([item['id'] for item in response.json()]) == []
        else:
            values_list = Invite.objects.filter(project_id=project_id) \
                                        .order_by('id').values_list('id', flat=True)
            assert sorted([item['id'] for item in response.json()]) == list(values_list)
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('invite_id', invites)
def test_detail(db, client, username, password, project_id, invite_id):
    client.login(username=username, password=password)
    invite = Invite.objects.filter(project_id=project_id, id=invite_id).first()

    url = reverse(urlnames['detail'], args=[project_id, invite_id])
    response = client.get(url)

    if invite and project_id in view_invite_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') == invite_id
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_create_user(db, client, username, password, project_id):
    client.login(username=username, password=password)

    user = get_user_model().objects.get(username='user')

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'user': user.pk,
        'role': 'guest'
    }
    response = client.post(url, data)

    if project_id in add_invite_permission_map.get(username, []):
        assert response.status_code == 201
    elif project_id in view_invite_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_create_email(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'email': 'user@example.com',
        'role': 'guest'
    }
    response = client.post(url, data)

    if project_id in add_invite_permission_map.get(username, []):
        assert response.status_code == 201
    elif project_id in view_invite_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


def test_create_error(db, client):
    client.login(username='owner', password='owner')

    url = reverse(urlnames['list'], args=[1])
    data = {
        'role': 'guest'
    }
    response = client.post(url, data)
    assert response.status_code == 400
    assert response.json()['non_field_errors'][0] == 'Either user or e-mail needs to be provided.'


def test_create_error_user(db, client):
    client.login(username='owner', password='owner')

    url = reverse(urlnames['list'], args=[1])
    data = {
        'user': 800,
        'role': 'guest'
    }
    response = client.post(url, data)
    assert response.status_code == 400
    assert 'Invalid pk' in response.json()['user'][0]


def test_create_error_user_and_email(db, client):
    client.login(username='owner', password='owner')

    url = reverse(urlnames['list'], args=[1])
    data = {
        'user': 1,
        'email': 'user@example.com',
        'role': 'guest'
    }
    response = client.post(url, data)
    assert response.status_code == 400
    assert response.json()['non_field_errors'][0] == 'User and e-mail are mutually exclusive.'


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('invite_id', invites)
def test_update(db, client, username, password, project_id, invite_id):
    client.login(username=username, password=password)
    invite = Invite.objects.filter(project_id=project_id, id=invite_id).first()

    url = reverse(urlnames['detail'], args=[project_id, invite_id])
    data = {
        'role': 'guest'
    }
    response = client.put(url, data, content_type='application/json')

    if invite and project_id in change_invite_permission_map.get(username, []):
        assert response.status_code == 200
    elif invite and project_id in view_invite_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('invite_id', invites)
def test_delete(db, client, username, password, project_id, invite_id):
    client.login(username=username, password=password)
    invite = Invite.objects.filter(project_id=project_id, id=invite_id).first()

    url = reverse(urlnames['detail'], args=[project_id, invite_id])
    response = client.delete(url)

    if invite and project_id in delete_invite_permission_map.get(username, []):
        assert response.status_code == 204
    elif invite and project_id in view_invite_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404
