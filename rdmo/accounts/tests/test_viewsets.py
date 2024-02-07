import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

users = (
    ('site', 'site'),  # site manager for all sites
    ('editor', 'editor'),  # editor for all sites
    ('reviewer', 'reviewer'),  # reviewer for all sites
    ('api', 'api'),  # has all roles for all sites, same as superuser
    ('admin', 'admin'),  # superuser
    ('user', 'user'),
    ('anonymous', None)
)

more_example_users = (
    'example-user',
    'example-manager',
    'example-editor',
    'example-reviewer'
)

members_from_other_sites = (
    'other',
    'foo-user',
    'foo-manager',
    'foo-editor',
    'foo-reviewer',
    'bar-user',
    'bar-manager',
    'bar-editor',
    'bar-reviewer',
)

status_map = {
    'list': {
        'editor': 403,  'reviewer': 403, 'site': 403, 'api': 403, 'user': 403, 'anonymous': 401, 'admin' : 200
    },
    'detail': {
        'editor': 404,  'reviewer': 404, 'site': 404, 'api': 404, 'user': 404, 'anonymous': 401, 'admin' : 200
    },
    'create': {
        'editor': 403,  'reviewer': 403, 'site': 403, 'api': 403, 'user': 403, 'anonymous': 401, 'admin' : 405
    },
    'update': {
        'editor': 405,  'reviewer': 405, 'site': 405, 'api': 405, 'user': 405, 'anonymous': 401, 'admin' : 405
    },
    'delete': {
        'editor': 405,  'reviewer': 405, 'site': 405, 'api': 405, 'user': 405, 'anonymous': 401, 'admin' : 405
    }
}

urlnames = {
    'list': 'v1-accounts:user-list',
    'detail': 'v1-accounts:user-detail'
}


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()
    if response.status_code == 200:
        if username == 'api' or username == 'admin':
            assert len(response.json()) == get_user_model().objects.count()
        elif username == 'site':
            # the site manager for example.com must see only the members of example.com
            assert len(response.json()) == get_user_model().objects.count() - len(members_from_other_sites)
        else:
            assert len(response.json()) == 0


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = get_user_model().objects.all()
    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        if username == 'site' and not instance.role.member.filter(domain__contains='example.com').exists():
            # the site manager for example.com must see only the members of example.com
            assert response.status_code == 404, response.json()
        else:
            assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.post(url, {})
    assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = get_user_model().objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.put(url, {}, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = get_user_model().objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()
