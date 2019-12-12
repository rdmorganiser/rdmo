import pytest
from django.urls import reverse

from ..models import Membership, Project

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),
    ('anonymous', None),
)

status_map = {
    'create_get': {
        'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
    },
    'create_post': {
        'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
    },
    'update_get': {
        'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
    },
    'update_post': {
        'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
    },
    'delete_get': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 403, 'user': 403, 'anonymous': 302
    },
    'delete_post': {
        'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'anonymous': 302
    }
}

urlnames = {
    'create': 'membership_create',
    'update': 'membership_update',
    'delete': 'membership_delete'
}

project_pk = 1

membership_roles = ('owner', 'manager', 'author', 'guest')


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
def test_membership_update_get(db, client, username, password):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_pk)
    memberships = Membership.objects.filter(project=project)

    for membership in memberships:
        url = reverse(urlnames['update'], args=[project_pk, membership.pk])
        response = client.get(url)
        assert response.status_code == status_map['update_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_membership_update_post(db, client, username, password):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_pk)
    memberships = Membership.objects.filter(project=project)

    for membership in memberships:
        url = reverse(urlnames['update'], args=[project_pk, membership.pk])
        data = {
            'user': membership.user,
            'role': membership.role
        }
        response = client.post(url, data)
        assert response.status_code == status_map['update_post'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_membership_delete_get(db, client, username, password):
    client.login(username=username, password=password)
    snapshot = Project.objects.get(pk=project_pk).snapshots.first()

    url = reverse(urlnames['delete'], args=[project_pk, snapshot.pk])
    response = client.get(url)
    assert response.status_code == status_map['delete_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_membership_delete_post(db, client, username, password):
    client.login(username=username, password=password)
    snapshot = Project.objects.get(pk=project_pk).snapshots.first()

    url = reverse(urlnames['delete'], args=[project_pk, snapshot.pk])
    response = client.post(url)
    assert response.status_code == status_map['delete_post'][username], response.content
