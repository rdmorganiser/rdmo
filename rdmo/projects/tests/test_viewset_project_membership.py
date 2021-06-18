import pytest
from django.contrib.auth import get_user_model
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
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'guest': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

add_membership_permission_map = change_membership_permission_map = delete_membership_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

urlnames = {
    'list': 'v1-projects:project-membership-list',
    'detail': 'v1-projects:project-membership-detail'
}

projects = [1, 2, 3, 4, 5]
memberships = [1, 2, 3, 4]
membership_roles = ('owner', 'manager', 'author', 'guest')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_list(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    response = client.get(url)

    if project_id in view_membership_permission_map.get(username, []):
        assert response.status_code == 200

        if username == 'user':
            assert sorted([item['id'] for item in response.json()]) == []
        else:
            values_list = Membership.objects.filter(project_id=project_id) \
                                            .order_by('id').values_list('id', flat=True)
            assert sorted([item['id'] for item in response.json()]) == list(values_list)
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('membership_id', memberships)
def test_detail(db, client, username, password, project_id, membership_id):
    client.login(username=username, password=password)
    membership = Membership.objects.filter(project_id=project_id, id=membership_id).first()

    url = reverse(urlnames['detail'], args=[project_id, membership_id])
    response = client.get(url)

    if membership and project_id in view_membership_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') == membership_id
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('membership_role', membership_roles)
def test_create(db, client, username, password, project_id, membership_role):
    client.login(username=username, password=password)

    user = get_user_model().objects.get(username='user')

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'user': user.pk,
        'role': membership_role
    }
    response = client.post(url, data)

    if project_id in add_membership_permission_map.get(username, []):
        assert response.status_code == 201
    elif project_id in view_membership_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('membership_id', memberships)
@pytest.mark.parametrize('membership_role', membership_roles)
def test_update(db, client, username, password, project_id, membership_id, membership_role):
    client.login(username=username, password=password)
    membership = Membership.objects.filter(project_id=project_id, id=membership_id).first()

    url = reverse(urlnames['detail'], args=[project_id, membership_id])
    data = {
        'role': membership_role
    }
    response = client.put(url, data, content_type='application/json')

    if membership and project_id in change_membership_permission_map.get(username, []):
        assert response.status_code == 200
    elif membership and project_id in view_membership_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('membership_id', memberships)
def test_delete(db, client, username, password, project_id, membership_id):
    client.login(username=username, password=password)
    membership = Membership.objects.filter(project_id=project_id, id=membership_id).first()

    url = reverse(urlnames['detail'], args=[project_id, membership_id])
    response = client.delete(url)

    if membership and project_id in delete_membership_permission_map.get(username, []):
        assert response.status_code == 204
    elif membership and project_id in view_membership_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404
