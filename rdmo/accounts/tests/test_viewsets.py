import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

users = (
    ('site', 'site'),  # site manager for example.com
    ('editor', 'editor'),  # site editor for example.com
    ('api', 'api'),
    ('user', 'user'),
    ('anonymous', None),
)

members_from_other_sites = (
    'other',
    'foo-user',
    'foo-manager',
    'foo-editor',
    'bar-user',
    'bar-manager',
    'bar-editor',
)

status_map = {
    'list': {
        'site': 200, 'api': 200, 'user': 200, 'anonymous': 401
    },
    'detail': {
        'site': 200, 'api': 200, 'user': 404, 'anonymous': 401
    },
    'create': {
        'site': 405, 'api': 405, 'user': 405, 'anonymous': 401
    },
    'update': {
        'site': 405, 'api': 405, 'user': 405, 'anonymous': 401
    },
    'delete': {
        'site': 405, 'api': 405, 'user': 405, 'anonymous': 401
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
        if username == 'api':
            assert len(response.json()) == get_user_model().objects.count()
        elif username == 'site':
            # the site admin must not see the user 'other' and not foo-editor and not bar-editor
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
        if username == 'site' and instance.username in members_from_other_sites:
            # the site admin must not see the user 'members_from_other_sites'
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
