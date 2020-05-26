import pytest
from django.urls import reverse

from ..models import Membership, Project

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

status_map = {
    'create_get': {
        'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'create_post': {
        'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'site': 302, 'anonymous': 302
    },
    'update_get': {
        'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'update_post': {
        'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'site': 302, 'anonymous': 302
    },
    'delete_get': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'delete_post': {
        'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'site': 302, 'anonymous': 302
    }
}

urlnames = {
    'create': 'membership_create',
    'update': 'membership_update',
    'delete': 'membership_delete'
}

project_pk = 1

membership_roles = ('owner', 'manager', 'author', 'guest')
membership_users = ('owner', 'manager', 'author', 'guest')


@pytest.mark.parametrize('username,password', users)
def test_membership_create_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['create'], args=[project_pk])
    response = client.get(url)
    assert response.status_code == status_map['create_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('role', membership_roles)
def test_membership_create_post(db, client, username, password, role):
    client.login(username=username, password=password)

    url = reverse(urlnames['create'], args=[project_pk])
    data = {
        'username_or_email': 'user',
        'role': role
    }
    response = client.post(url, data)
    assert response.status_code == status_map['create_post'][username], response.content
    if password and response.status_code == 302:
        assert Membership.objects.filter(user__username='user', role=role).exists()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('membership_username', membership_users)
def test_membership_update_get(db, client, username, password, membership_username):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_pk)
    membership = Membership.objects.filter(project=project).get(user__username=membership_username)

    url = reverse(urlnames['update'], args=[project_pk, membership.pk])
    response = client.get(url)
    assert response.status_code == status_map['update_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('membership_username', membership_users)
def test_membership_update_post(db, client, username, password, membership_username):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_pk)
    membership = Membership.objects.filter(project=project).get(user__username=membership_username)

    url = reverse(urlnames['update'], args=[project_pk, membership.pk])
    data = {
        'user': membership.user,
        'role': membership.role
    }
    response = client.post(url, data)
    assert response.status_code == status_map['update_post'][username], response.content


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('membership_username', membership_users)
def test_membership_delete_get(db, client, username, password, membership_username):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_pk)
    membership = Membership.objects.filter(project=project).get(user__username=membership_username)

    url = reverse(urlnames['delete'], args=[project_pk, membership.pk])
    response = client.get(url)

    if membership_username == username:
        assert response.status_code == 200, (membership, response.content)
    else:
        assert response.status_code == status_map['delete_get'][username], (membership, response.content)


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('membership_username', membership_users)
def test_membership_delete_post(db, client, mocker, username, password, membership_username):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_pk)
    membership = Membership.objects.filter(project=project).get(user__username=membership_username)

    url = reverse(urlnames['delete'], args=[project_pk, membership.pk])
    response = client.post(url)

    if membership_username == username:
        status_code = 400 if (membership_username == 'owner') else 302
        assert response.status_code == status_code, (membership, response.content)
    else:
        status_code = 400 if (membership_username == 'owner' and username == 'site') else status_map['delete_post'][username]
        assert response.status_code == status_code, (membership, response.content)
