import pytest

from django.urls import reverse

from ..models import Membership

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

view_membership_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10],
    'manager': [1, 3, 5, 7],
    'author': [1, 3, 5, 8],
    'guest': [1, 3, 5, 9],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}

urlnames = {
    'list': 'v1-projects:membership-list',
    'detail': 'v1-projects:membership-detail'
}

projects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
memberships = [1, 2, 3, 4]
membership_roles = ('owner', 'manager', 'author', 'guest')


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
            values_list = Membership.objects.filter(project__in=view_membership_permission_map.get(username, [])) \
                                            .order_by('id').values_list('id', flat=True)
            assert sorted([item['id'] for item in response.json()]) == list(values_list)
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('membership_id', memberships)
def test_detail(db, client, username, password, membership_id):
    client.login(username=username, password=password)
    membership = Membership.objects.get(id=membership_id)

    url = reverse(urlnames['detail'], args=[membership_id])
    response = client.get(url)

    if membership.project.id in view_membership_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') == membership_id
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
@pytest.mark.parametrize('membership_id', memberships)
def test_update(db, client, username, password, membership_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[membership_id])
    data = {}
    response = client.put(url, data, content_type='application/json')

    if password:
        assert response.status_code == 405
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('membership_id', memberships)
def test_delete(db, client, username, password, membership_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[membership_id])
    response = client.delete(url)

    if password:
        assert response.status_code == 405
    else:
        assert response.status_code == 401
