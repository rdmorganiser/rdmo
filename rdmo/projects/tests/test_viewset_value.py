import pytest
from django.urls import reverse

from rdmo.core.constants import VALUE_TYPE_FILE

from ..models import Value

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
    'list': 'v1-projects:value-list',
    'detail': 'v1-projects:value-detail',
    'file': 'v1-projects:value-file'
}

site_id = 1
project_id = 1


def assert_value(username, value):
    if username == 'api':
        assert value['id'] in Value.objects.values_list('id', flat=True)
    elif username == 'site':
        assert value['id'] in Value.objects.filter(project__site_id=site_id).values_list('id', flat=True)
    else:
        assert value['id'] in Value.objects.filter(project__user__username=username).values_list('id', flat=True)


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()

    if response.status_code == 200:
        for value in response.json():
            assert_value(username, value)


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = Value.objects.filter(project_id=project_id, snapshot=None)

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()

        if response.status_code == 200:
            assert_value(username, response.json())


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = Value.objects.filter(project_id=project_id, snapshot=None)

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'project': instance.project.pk,
            'snapshot': instance.snapshot.pk if instance.snapshot else '',
            'attribute': instance.attribute.pk,
            'set_index': instance.set_index,
            'collection_index': instance.collection_index,
            'text': instance.text,
            'option': instance.option.pk if instance.option else '',
            'value_type': instance.value_type,
            'unit': instance.unit
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = Value.objects.filter(project_id=project_id, snapshot=None)

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'project': instance.project.pk,
            'snapshot': instance.snapshot.pk if instance.snapshot else None,
            'attribute': instance.attribute.pk,
            'set_index': instance.set_index,
            'collection_index': instance.collection_index,
            'text': instance.text,
            'option': instance.option.pk if instance.option else None,
            'value_type': instance.value_type,
            'unit': instance.unit
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = Value.objects.filter(project_id=project_id, snapshot=None)

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_file(db, client, files, username, password):
    client.login(username=username, password=password)
    instances = Value.objects.filter(project_id=project_id, snapshot=None)

    for instance in instances:
        url = reverse(urlnames['file'], args=[instance.pk])
        response = client.get(url)

        if instance.value_type == VALUE_TYPE_FILE:
            assert response.status_code == status_map['detail'][username], response.json()

            if response.status_code == 200:
                assert response['Content-Type'] == instance.file_type
                assert response['Content-Disposition'] == 'attachment; filename={}'.format(instance.file_name)
                assert response.content == instance.file.read()
        else:
            assert response.status_code == 404 if password else 401
