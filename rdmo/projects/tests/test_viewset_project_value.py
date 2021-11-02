from pathlib import Path

import pytest
from django.conf import settings
from django.urls import reverse

from rdmo.core.constants import (VALUE_TYPE_CHOICES, VALUE_TYPE_FILE,
                                 VALUE_TYPE_TEXT)
from rdmo.questions.models import Question

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

view_value_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'guest': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

add_value_permission_map = change_value_permission_map = delete_value_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

urlnames = {
    'list': 'v1-projects:project-value-list',
    'detail': 'v1-projects:project-value-detail',
    'set': 'v1-projects:project-value-set',
    'file': 'v1-projects:project-value-file'
}

projects = [1, 2, 3, 4, 5]
values = [1, 2, 3, 4, 5, 6, 7, 238, 242, 247, 248, 249]

attribute_id = 1
option_id = 1

set_values = [84, 85]
set_questionsets = [42, 43]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_list(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    response = client.get(url)

    if project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        if username == 'user':
            assert sorted([item['id'] for item in response.json()]) == []
        else:
            values_list = Value.objects.filter(project_id=project_id) \
                                       .filter(snapshot_id=None) \
                                       .order_by('id').values_list('id', flat=True)
            assert sorted([item['id'] for item in response.json()]) == list(values_list)

    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('value_id', values)
def test_detail(db, client, username, password, project_id, value_id):
    client.login(username=username, password=password)
    value = Value.objects.filter(project_id=project_id, id=value_id).filter()

    url = reverse(urlnames['detail'], args=[project_id, value_id])
    response = client.get(url)

    if value and project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') == value_id
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('value_type,value_type_label', VALUE_TYPE_CHOICES)
def test_create_text(db, client, username, password, project_id, value_type, value_type_label):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'attribute': attribute_id,
        'set_index': 0,
        'collection_index': 0,
        'text': 'Lorem ipsum',
        'value_type': value_type,
        'unit': ''
    }
    response = client.post(url, data)

    if project_id in add_value_permission_map.get(username, []):
        assert response.status_code == 201
        assert isinstance(response.json(), dict)
        assert response.json().get('id') in Value.objects.filter(project_id=project_id).values_list('id', flat=True)
    elif project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('value_type,value_type_label', VALUE_TYPE_CHOICES)
def test_create_option(db, client, username, password, project_id, value_type, value_type_label):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'attribute': attribute_id,
        'set_index': 0,
        'collection_index': 0,
        'option': option_id,
        'value_type': value_type,
        'unit': ''
    }
    response = client.post(url, data)

    if project_id in add_value_permission_map.get(username, []):
        assert response.status_code == 201
        assert isinstance(response.json(), dict)
        assert response.json().get('id') in Value.objects.filter(project_id=project_id).values_list('id', flat=True)
    elif project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('value_type,value_type_label', VALUE_TYPE_CHOICES)
def test_create_external(db, client, username, password, project_id, value_type, value_type_label):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'attribute': attribute_id,
        'set_index': 0,
        'collection_index': 0,
        'text': 'Lorem ipsum',
        'external_id': '1',
        'value_type': value_type,
        'unit': ''
    }
    response = client.post(url, data)

    if project_id in add_value_permission_map.get(username, []):
        assert response.status_code == 201
        assert isinstance(response.json(), dict)
        assert response.json().get('id') in Value.objects.filter(project_id=project_id).values_list('id', flat=True)
    elif project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('value_id', values)
def test_update(db, client, username, password, project_id, value_id):
    client.login(username=username, password=password)
    value = Value.objects.filter(project_id=project_id, id=value_id).first()

    url = reverse(urlnames['detail'], args=[project_id, value_id])
    data = {
        'attribute': attribute_id,
        'set_index': 0,
        'collection_index': 0,
        'text': 'Lorem ipsum',
        'value_type': VALUE_TYPE_TEXT,
        'unit': ''
    }
    response = client.put(url, data, content_type='application/json')

    if value and project_id in change_value_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') in Value.objects.filter(project_id=project_id).values_list('id', flat=True)
    elif value and project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('value_id', values)
def test_delete(db, client, username, password, project_id, value_id):
    client.login(username=username, password=password)
    value = Value.objects.filter(project_id=project_id, id=value_id).first()

    url = reverse(urlnames['detail'], args=[project_id, value_id])
    response = client.delete(url)

    if value and project_id in delete_value_permission_map.get(username, []):
        assert response.status_code == 204
        assert not Value.objects.filter(pk=value_id).exists()
    elif value and project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 403
        assert Value.objects.filter(pk=value_id).exists()
    else:
        assert response.status_code == 404
        assert Value.objects.filter(pk=value_id).exists()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('value_id', set_values)
def test_set(db, client, username, password, project_id, value_id):
    client.login(username=username, password=password)
    value = Value.objects.filter(project_id=project_id, snapshot=None, id=value_id).first()

    set_attributes = Question.objects.filter(questionset__id__in=set_questionsets).values_list('attribute', flat=True)
    values_count = Value.objects.count()
    if value and project_id in delete_value_permission_map.get(username, []):
        set_values_count = Value.objects.filter(project_id=project_id,
                                                snapshot=None,
                                                attribute__in=set_attributes,
                                                set_index=value.set_index).count()

    url = reverse(urlnames['set'], args=[project_id, value_id])
    response = client.delete(url)

    if value and project_id in delete_value_permission_map.get(username, []):
        assert response.status_code == 204
        assert not Value.objects.filter(pk=value_id).exists()
        assert Value.objects.count() == values_count - set_values_count - 1  # one is for set/id
    elif value and project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 403
        assert Value.objects.filter(pk=value_id).exists()
        assert Value.objects.count() == values_count
    else:
        assert response.status_code == 404
        assert Value.objects.filter(pk=value_id).exists()
        assert Value.objects.count() == values_count


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('value_id', values)
def test_file_get(db, client, files, username, password, project_id, value_id):
    client.login(username=username, password=password)
    value = Value.objects.filter(project_id=project_id, id=value_id).first()

    url = reverse(urlnames['file'], args=[project_id, value_id])
    response = client.get(url)

    if value and value.value_type == VALUE_TYPE_FILE and project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 200
        assert response['Content-Type'] == value.file_type
        assert response['Content-Disposition'] == 'attachment; filename={}'.format(value.file_name)
        assert response.content == value.file.read()
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('value_id', values)
def test_file_put(db, client, files, username, password, project_id, value_id):
    client.login(username=username, password=password)
    value = Value.objects.filter(project_id=project_id, id=value_id).first()

    url = reverse(urlnames['file'], args=[project_id, value_id])

    file_path = Path(settings.MEDIA_ROOT) / 'test_file.txt'
    with file_path.open() as fp:
        response = client.post(url, {'name': 'test_file.txt', 'file': fp})

    if value and project_id in change_value_permission_map.get(username, []):
        assert response.status_code == 200
        assert response.json().get('file_name') == 'test_file.txt'
    elif value and project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404
