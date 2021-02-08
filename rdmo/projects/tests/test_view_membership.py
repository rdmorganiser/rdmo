import pytest
from django.urls import reverse

from ..models import Membership

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

add_membership_permission_map = change_membership_permission_map = delete_membership_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

projects = [1, 2, 3, 4, 5]
memberships = [1, 2, 3, 4]

membership_roles = ('owner', 'manager', 'author', 'guest')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_membership_create_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('membership_create', args=[project_id])
    response = client.get(url)

    if project_id in add_membership_permission_map.get(username, []):
        assert response.status_code == 200
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('membership_role', membership_roles)
def test_membership_create_post(db, client, username, password, project_id, membership_role):
    client.login(username=username, password=password)

    url = reverse('membership_create', args=[project_id])
    data = {
        'username_or_email': 'user',
        'role': membership_role
    }
    response = client.post(url, data)

    if project_id in add_membership_permission_map.get(username, []):
        assert response.status_code == 302
        assert Membership.objects.filter(project_id=project_id, user__username='user', role=membership_role).first()
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302

        assert not Membership.objects.filter(project_id=project_id, user__username='user', role=membership_role).first()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('membership_id', memberships)
def test_membership_update_get(db, client, username, password, project_id, membership_id):
    client.login(username=username, password=password)
    membership = Membership.objects.filter(project_id=project_id, id=membership_id).first()

    url = reverse('membership_update', args=[project_id, membership_id])
    response = client.get(url)

    if membership:
        if project_id in change_membership_permission_map.get(username, []):
            assert response.status_code == 200
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('membership_id', memberships)
@pytest.mark.parametrize('membership_role', membership_roles)
def test_membership_update_post(db, client, username, password, project_id, membership_id, membership_role):
    client.login(username=username, password=password)
    membership = Membership.objects.filter(project_id=project_id, id=membership_id).first()

    url = reverse('membership_update', args=[project_id, membership_id])
    data = {
        'role': membership_role
    }
    response = client.post(url, data)

    if membership:
        if project_id in change_membership_permission_map.get(username, []):
            assert response.status_code == 302
            assert Membership.objects.get(project_id=project_id, id=membership_id).role == membership_role

        else:
            if password:
                assert response.status_code == 403
            else:
                assert response.status_code == 302

            assert Membership.objects.get(project_id=project_id, id=membership_id).role == membership.role
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('membership_id', memberships)
def test_membership_delete_get(db, client, username, password, project_id, membership_id):
    client.login(username=username, password=password)
    membership = Membership.objects.filter(project_id=project_id, id=membership_id).first()

    url = reverse('membership_delete', args=[project_id, membership_id])
    response = client.get(url)

    if membership:
        if project_id in delete_membership_permission_map.get(username, []):
            assert response.status_code == 200
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('membership_id', memberships)
def test_membership_delete_post(db, client, mocker, username, password, project_id, membership_id):
    client.login(username=username, password=password)
    membership = Membership.objects.filter(project_id=project_id, id=membership_id).first()

    url = reverse('membership_delete', args=[project_id, membership_id])
    response = client.post(url)

    if membership:
        if project_id in delete_membership_permission_map.get(username, []):
            if membership.user.username == 'owner':
                assert response.status_code == 400
            else:
                assert response.status_code == 302
                assert not Membership.objects.filter(project_id=project_id, id=membership_id).first()
        elif password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
    else:
        assert response.status_code == 404
