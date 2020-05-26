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

status_map = {
    'list': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 404
    },
    'detail': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 404
    },
    'create': {
        'owner': 201, 'manager': 403, 'author': 403, 'guest': 403, 'api': 201, 'user': 404, 'site': 201, 'anonymous': 404
    },
    'update': {
        'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 404
    },
    'delete': {
        'owner': 204, 'manager': 204, 'author': 204, 'guest': 204, 'api': 204, 'user': 404, 'site': 204, 'anonymous': 404
    }
}

urlnames = {
    'list': 'v1-projects:project-membership-list',
    'detail': 'v1-projects:project-membership-detail'
}

site_id = 1
project_id = 1

membership_roles = ('owner', 'manager', 'author', 'guest')
membership_users = ('owner', 'manager', 'author', 'guest')


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('membership_username', membership_users)
def test_detail(db, client, username, password, membership_username):
    client.login(username=username, password=password)
    instance = Membership.objects.filter(project_id=project_id).get(user__username=membership_username)

    url = reverse(urlnames['detail'], args=[project_id, instance.pk])
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('membership_username', membership_users)
def test_create(db, client, username, password, membership_username):
    client.login(username=username, password=password)
    instance = Membership.objects.filter(project_id=project_id).get(user__username=membership_username)

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'user': instance.user.pk,
        'role': instance.role
    }
    response = client.post(url, data)
    assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('membership_username', membership_users)
def test_update(db, client, username, password, membership_username):
    client.login(username=username, password=password)
    instance = Membership.objects.filter(project_id=project_id).get(user__username=membership_username)

    url = reverse(urlnames['detail'], args=[project_id, instance.pk])
    data = {
        'user': instance.user.pk,
        'role': instance.role
    }
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == status_map['update'][username], response.json()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('membership_username', membership_users)
def test_delete(db, client, username, password, membership_username):
    client.login(username=username, password=password)
    instance = Membership.objects.filter(project_id=project_id).get(user__username=membership_username)

    url = reverse(urlnames['detail'], args=[project_id, instance.pk])
    response = client.delete(url)
    assert response.status_code == status_map['delete'][username], response.content
