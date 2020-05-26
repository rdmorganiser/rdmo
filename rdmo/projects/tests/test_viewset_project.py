import pytest
from django.urls import reverse
from rdmo.conditions.models import Condition

from ..models import Project

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
        'owner': 201, 'manager': 201, 'author': 201, 'guest': 201, 'api': 201, 'user': 201, 'site': 201, 'anonymous': 401
    },
    'update': {
        'owner': 200, 'manager': 200, 'author': 403, 'guest': 403, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 401
    },
    'delete': {
        'owner': 204, 'manager': 403, 'author': 403, 'guest': 403, 'api': 204, 'user': 404, 'site': 204, 'anonymous': 401
    },
    'resolve': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'api': 200, 'user': 404, 'site': 200, 'anonymous': 401
    },
}

urlnames = {
    'list': 'v1-projects:project-list',
    'detail': 'v1-projects:project-detail',
    'resolve': 'v1-projects:project-resolve'
}

site_id = 1
project_id = 1


def assert_project(username, value):
    assert isinstance(value, dict)

    if username == 'api':
        assert value['id'] in Project.objects.values_list('id', flat=True)
    elif username == 'site':
        assert value['id'] in Project.objects.filter(site_id=site_id).values_list('id', flat=True)
    else:
        assert value['id'] in Project.objects.filter(user__username=username).values_list('id', flat=True)


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()

    if response.status_code == 200:
        assert isinstance(response.json(), list)

        for project in response.json():
            assert_project(username, project)


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Project.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()

        if response == 200:
            assert_project(username, response.json())


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Project.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'title': instance.title,
            'description': instance.description,
            'catalog': instance.catalog.pk
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()

        if response == 201:
            assert_project(username, response.json())


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Project.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'title': instance.title,
            'description': instance.description,
            'catalog': instance.catalog.pk
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()

        if response == 200:
            assert_project(username, response.json())


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Project.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()

        if response.status_code == 204:
            assert not Project.objects.filter(pk=instance.pk).exists()
        else:
            assert Project.objects.filter(pk=instance.pk).exists()


@pytest.mark.parametrize('username,password', users)
def test_resolve(db, client, username, password):
    client.login(username=username, password=password)
    instances = Project.objects.all()
    conditions = Condition.objects.all()

    for instance in instances:
        url = reverse(urlnames['resolve'], args=[instance.pk])

        for condition in conditions:
            response = client.get(url + '?condition={}'.format(condition.pk))
            assert response.status_code == status_map['resolve'][username], response.json()
