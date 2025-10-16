import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Membership, Project

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
    'owner': [1, 2, 3, 4, 5, 12],
    'manager': [1, 3, 5, 12],
    'author': [1, 3, 5, 12],
    'guest': [1, 3, 5, 12],
    'user': [12],
    'api': [1, 2, 3, 4, 5, 12],
    'site': [1, 2, 3, 4, 5, 12]
}

add_membership_permission_map = {
    'api': [1, 2, 3, 4, 5, 12],
    'site': [1, 2, 3, 4, 5, 12]
}

change_membership_permission_map = delete_membership_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'api': [1, 2, 3, 4, 5, 12],
    'site': [1, 2, 3, 4, 5, 12]
}

urlnames = {
    'list': 'v1-projects:project-membership-list',
    'detail': 'v1-projects:project-membership-detail'
}

projects = [1, 2, 3, 4, 5, 12]
memberships = [1, 2, 3, 4]
memberships_visible = [16]
membership_roles = ('owner', 'manager', 'author', 'guest')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_list(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    response = client.get(url)

    if project_id in view_membership_permission_map.get(username, []):
        assert response.status_code == 200

        response_data = response.json()

        if username == 'user':
            assert sorted([item['id'] for item in response_data]) == memberships_visible
            assert all('user' in item for item in response_data)
            assert all('email' in item['user'] for item in response_data)
        else:
            values_list = Membership.objects.filter(project_id=project_id) \
                                            .order_by('id').values_list('id', flat=True)
            assert sorted([item['id'] for item in response_data]) == list(values_list)
            assert all('user' in item for item in response_data)
            assert all('email' in item['user'] for item in response_data)
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('membership_id', memberships)
def test_detail(db, client, username, password, membership_id):
    client.login(username=username, password=password)
    membership = Membership.objects.get(id=membership_id)

    url = reverse(urlnames['detail'], args=[membership.project_id, membership_id])
    response = client.get(url)

    if membership.project_id in view_membership_permission_map.get(username, []):
        assert response.status_code == 200

        response_data = response.json()

        assert isinstance(response_data, dict)
        assert response_data['id'] == membership_id
        assert response_data['user']['id'] == membership.user.id
        assert response_data['user']['email'] == membership.user.email

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
@pytest.mark.parametrize('membership_role', membership_roles)
def test_create_lookup(db, client, username, password, project_id, membership_role):
    if password:
        client.login(username=username, password=password)
        user = get_user_model().objects.get(username=username)
        already_a_member = Project.objects.get(id=project_id).memberships.filter(user=user).exists()

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'lookup': username,  # valid test username
        'role': membership_role
    }
    response = client.post(url, data)

    if project_id in add_membership_permission_map.get(username, []):
        if already_a_member:
            assert response.status_code == 400
            assert 'already a member' in response.json()['non_field_errors'][0]
        else:
            assert response.status_code == 201

            response_data = response.json()

            assert response_data['id']
            assert response_data['role'] == membership_role
            assert response_data['user']['first_name']
            assert response_data['user']['last_name']
    elif project_id in view_membership_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('lookup,expected_error', [
    ('nosuchuser', 'No user found.'),
    ('bad@mail', 'Enter a valid email address.'),
])
def test_create_lookup_error_invalid(db, client, lookup, expected_error):
    client.login(username='site', password='site')
    url = reverse(urlnames['list'], args=[1])

    data = {
        'lookup': lookup,
        'role': 'guest'
    }
    response = client.post(url, data)
    assert response.status_code == 400
    err = response.json()
    assert 'lookup' in err
    assert err['lookup'][0] == expected_error


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('membership_id', memberships)
@pytest.mark.parametrize('membership_role', membership_roles)
def test_update(db, client, username, password, membership_id, membership_role):
    client.login(username=username, password=password)
    membership = Membership.objects.get(id=membership_id)

    url = reverse(urlnames['detail'], args=[membership.project_id, membership_id])
    data = {
        'role': membership_role
    }
    response = client.put(url, data, content_type='application/json')

    if membership.project_id in change_membership_permission_map.get(username, []):
        assert response.status_code == 200
    elif membership.project_id in view_membership_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('membership_id', memberships)
def test_delete(db, client, username, password, membership_id):
    client.login(username=username, password=password)
    membership = Membership.objects.get(id=membership_id)

    url = reverse(urlnames['detail'], args=[membership.project_id, membership_id])
    response = client.delete(url)

    if membership.project_id in change_membership_permission_map.get(username, []):
        assert response.status_code == 204
    elif membership.project_id in view_membership_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404
