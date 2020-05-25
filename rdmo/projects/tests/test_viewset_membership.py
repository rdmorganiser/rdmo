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
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 200, 'site': 200, 'anonymous': 401
    },
    'detail': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 401
    },
    'create': {
        'owner': 405, 'manager': 405, 'author': 405, 'guest': 405, 'api': 405, 'user': 405, 'site': 405, 'anonymous': 401
    },
    'update': {
        'owner': 405, 'manager': 405, 'author': 405, 'guest': 405, 'api': 405, 'user': 405, 'site': 405, 'anonymous': 401
    },
    'delete': {
        'owner': 405, 'manager': 405, 'author': 405, 'guest': 405, 'api': 405, 'user': 405, 'site': 405, 'anonymous': 401
    }
}

urlnames = {
    'list': 'v1-projects:membership-list',
    'detail': 'v1-projects:membership-detail'
}

site_id = 1
project_id = 1

membership_roles = ('owner', 'manager', 'author', 'guest')
membership_users = ('owner', 'manager', 'author', 'guest')


def assert_membership(username, value):
    assert isinstance(value, dict)

    if username == 'api':
        assert value['id'] in Membership.objects.values_list('id', flat=True)
    elif username == 'site':
        assert value['id'] in Membership.objects.filter(project__site_id=site_id).values_list('id', flat=True)
    else:
        assert value['id'] in Membership.objects.filter(project__user__username=username).values_list('id', flat=True)


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()

    if response.status_code == 200:
        assert isinstance(response.json(), list)

        for membership in response.json():
            assert_membership(username, membership)


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Membership.objects.filter(project_id=project_id)

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()

        if response == 200:
            assert_membership(username, response.json())


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Membership.objects.filter(project_id=project_id)

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'project': project_id,
            'user': instance.user.pk,
            'role': instance.role
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()

        if response == 201:
            assert_membership(username, response.json())


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Membership.objects.filter(project_id=project_id)

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'project': project_id,
            'user': instance.user.pk,
            'role': instance.role
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()

        if response == 200:
            assert_membership(username, response.json())


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Membership.objects.filter(project_id=project_id).exclude(user__username=username)

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()

        if response.status_code == 204:
            assert not Membership.objects.filter(pk=instance.pk).exists()
        else:
            assert Membership.objects.filter(pk=instance.pk).exists()
