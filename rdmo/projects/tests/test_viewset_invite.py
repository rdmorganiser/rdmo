import pytest

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

view_issue_permission_map = {
    'owner': [1],
    'manager': [],
    'author': [],
    'guest': [],
    'api': [1, 11],
    'site': [1, 11]
}

urlnames = {
    'list': 'v1-projects:invite-list',
    'detail': 'v1-projects:invite-detail'
}

invites = [1, 2]


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)

    if password:
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        if username == 'user':
            assert sorted([item['id'] for item in response.json()]) == []
        else:
            values_list = Invite.objects.filter(project__in=view_issue_permission_map.get(username, [])) \
                                        .order_by('id').values_list('id', flat=True)
            assert sorted([item['id'] for item in response.json()]) == list(values_list)
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('invite_id', invites)
def test_detail(db, client, username, password, invite_id):
    client.login(username=username, password=password)
    invite = Invite.objects.get(id=invite_id)

    url = reverse(urlnames['detail'], args=[invite_id])
    response = client.get(url)

    if invite.project.id in view_issue_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') == invite_id
    elif password:
        assert response.status_code == 404
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.post(url)

    if password:
        assert response.status_code == 405
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('invite_id', invites)
def test_update(db, client, username, password, invite_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[invite_id])
    data = {}
    response = client.put(url, data, content_type='application/json')

    if password:
        assert response.status_code == 405
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('invite_id', invites)
def test_delete(db, client, username, password, invite_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[invite_id])
    response = client.delete(url)

    if password:
        assert response.status_code == 405
    else:
        assert response.status_code == 401
