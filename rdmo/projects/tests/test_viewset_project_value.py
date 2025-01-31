import json
from pathlib import Path

import pytest

from django.conf import settings
from django.urls import reverse

from rdmo.core.constants import VALUE_TYPE_FILE, VALUE_TYPE_TEXT

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
    'owner': [1, 2, 3, 4, 5, 12],
    'manager': [1, 3, 5, 12],
    'author': [1, 3, 5, 12],
    'guest': [1, 3, 5, 12],
    'user': [12],
    'api': [1, 2, 3, 4, 5, 12],
    'site': [1, 2, 3, 4, 5, 12]
}

add_value_permission_map = change_value_permission_map = delete_value_permission_map = copy_value_permission_map = {
    'owner': [1, 2, 3, 4, 5, 12],
    'manager': [1, 3, 5],
    'author': [1, 3, 5],
    'api': [1, 2, 3, 4, 5, 12],
    'site': [1, 2, 3, 4, 5, 12]
}

urlnames = {
    'list': 'v1-projects:project-value-list',
    'detail': 'v1-projects:project-value-detail',
    'copy-set': 'v1-projects:project-value-copy-set',
    'delete-set': 'v1-projects:project-value-delete-set',
    'file': 'v1-projects:project-value-file'
}

projects = [1, 2, 3, 4, 5, 12]
values = [
    1, 2, 3, 4, 5, 6, 7, 238,  # from Test <1>
    242,                       # from Parent <2>
    247,                       # from Child1 <3>
    248,                       # from Child2 <4>
    249,                       # from Child11 <5>
    456                        # from Internal <12>
]
values_internal = [456]

other_project_id = 11

attribute_id = 1
option_id = 1

set_values = [
    (84, 31),
    (85, 32)
]
set_questionsets = [42, 43]

value_texts = (
    ('text', 'Lorem ipsum'),
    ('url', 'https://lorem.ipsum'),
    ('integer', '1337'),
    ('float', '13.37'),
    ('boolean', '1'),
    ('datetime', '1337-01-13T13:37+13:37'),
    ('email', 'user@lorem.ipsum'),
    ('phone', '+49 (0) 1337 12345678')
)


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
            assert sorted([item['id'] for item in response.json()]) == values_internal
        else:
            values_list = Value.objects.filter(project_id=project_id) \
                                       .filter(snapshot_id=None) \
                                       .order_by('id').values_list('id', flat=True)
            assert sorted([item['id'] for item in response.json()]) == list(values_list)

    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('value_id', values)
def test_detail(db, client, username, password, value_id):
    client.login(username=username, password=password)
    value = Value.objects.get(id=value_id)

    url = reverse(urlnames['detail'], args=[value.project_id, value_id])
    response = client.get(url)

    if value.project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') == value_id
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('value_type,value_text', value_texts)
def test_create_text(db, client, username, password, project_id, value_type, value_text):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'attribute': attribute_id,
        'set_index': 0,
        'collection_index': 0,
        'text': value_text,
        'value_type': value_type,
        'unit': ''
    }
    response = client.post(url, data)

    if project_id in add_value_permission_map.get(username, []):
        assert response.status_code == 201, response.content
        assert isinstance(response.json(), dict)
        assert response.json().get('id') in Value.objects.filter(project_id=project_id).values_list('id', flat=True)
    elif project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('value_type,value_text', value_texts)
def test_create_option(db, client, username, password, project_id, value_type, value_text):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'attribute': attribute_id,
        'set_index': 0,
        'collection_index': 0,
        'text': value_text,
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
@pytest.mark.parametrize('value_type,value_text', value_texts)
def test_create_external(db, client, username, password, project_id, value_type, value_text):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'attribute': attribute_id,
        'set_index': 0,
        'collection_index': 0,
        'text': value_text,
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
@pytest.mark.parametrize('value_id', values)
def test_update(db, client, username, password, value_id):
    client.login(username=username, password=password)
    value = Value.objects.get(id=value_id)

    url = reverse(urlnames['detail'], args=[value.project_id, value_id])
    data = {
        'attribute': attribute_id,
        'set_index': 0,
        'collection_index': 0,
        'text': 'Lorem ipsum',
        'value_type': VALUE_TYPE_TEXT,
        'unit': ''
    }
    response = client.put(url, data, content_type='application/json')

    if value.project_id in change_value_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') in Value.objects.filter(project_id=value.project_id) \
                                                         .values_list('id', flat=True)
    elif value.project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('value_id', values)
def test_delete(db, client, username, password, value_id):
    client.login(username=username, password=password)
    value = Value.objects.get(id=value_id)

    url = reverse(urlnames['detail'], args=[value.project_id, value_id])
    response = client.delete(url)

    if value.project_id in delete_value_permission_map.get(username, []):
        assert response.status_code == 204
        assert not Value.objects.filter(pk=value_id).exists()
    elif value.project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 403
        assert Value.objects.filter(pk=value_id).exists()
    else:
        assert response.status_code == 404
        assert Value.objects.filter(pk=value_id).exists()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('value_id, set_values_count', set_values)
def test_copy_set(db, client, username, password, value_id, set_values_count):
    client.login(username=username, password=password)
    set_value = Value.objects.get(id=value_id)
    values_count = Value.objects.count()

    url = reverse(urlnames['copy-set'], args=[set_value.project_id])
    data = {
        'attribute': set_value.attribute.id,
        'set_prefix': set_value.set_prefix,
        'set_index': 2,
        'text': 'new'
    }
    response = client.post(url, data=json.dumps(dict(**data, copy_set_value=value_id)), content_type="application/json")

    if set_value.project_id in copy_value_permission_map.get(username, []):
        assert response.status_code == 201
        assert len(response.json()) == set_values_count + 1
        assert Value.objects.get(
            project=set_value.project_id,
            snapshot=None,
            **data
        )
        assert Value.objects.count() == values_count + set_values_count + 1  # one is for set/id
        for value_data in response.json():
            if value_data['set_prefix'] == data['set_prefix']:
                assert value_data['set_index'] == data['set_index']
            else:
                set_prefix_split = value_data['set_prefix'].split('|')
                assert set_prefix_split[0] == str(data['set_index'])

    elif set_value.project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 403
        assert Value.objects.count() == values_count
    else:
        assert response.status_code == 404
        assert Value.objects.count() == values_count


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('value_id, set_values_count', set_values)
def test_delete_set(db, client, username, password, project_id, value_id, set_values_count):
    client.login(username=username, password=password)
    value_exists = Value.objects.filter(project_id=project_id, snapshot=None, id=value_id).exists()
    values_count = Value.objects.count()

    url = reverse(urlnames['delete-set'], args=[project_id, value_id])
    response = client.delete(url)

    if value_exists and project_id in delete_value_permission_map.get(username, []):
        assert response.status_code == 204
        assert not Value.objects.filter(pk=value_id).exists()
        assert Value.objects.count() == values_count - set_values_count - 1  # one is for set/id
    elif value_exists and project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 403
        assert Value.objects.filter(pk=value_id).exists()
        assert Value.objects.count() == values_count
    else:
        assert response.status_code == 404
        assert Value.objects.filter(pk=value_id).exists()
        assert Value.objects.count() == values_count


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('value_id', values)
def test_file_get(db, client, files, username, password, value_id):
    client.login(username=username, password=password)
    value = Value.objects.get(id=value_id)

    url = reverse(urlnames['file'], args=[value.project_id, value_id])
    response = client.get(url)

    if value.value_type == VALUE_TYPE_FILE and value.project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 200
        assert response['Content-Type'] == value.file_type
        assert response['Content-Disposition'] == f'attachment; filename={value.file_name}'
        assert response.content == value.file.read()
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('value_id', values)
def test_file_put(db, client, files, username, password, value_id):
    client.login(username=username, password=password)
    value = Value.objects.get(id=value_id)

    url = reverse(urlnames['file'], args=[value.project_id, value_id])

    file_path = Path(settings.MEDIA_ROOT) / 'test_file.txt'
    with file_path.open() as fp:
        response = client.post(url, {'name': 'test_file.txt', 'file': fp})

    if value.project_id in change_value_permission_map.get(username, []):
        assert response.status_code == 200
        assert response.json().get('file_name') == 'test_file.txt'
    elif value.project_id in view_value_permission_map.get(username, []):
        assert response.status_code == 403
    else:
        assert response.status_code == 404
