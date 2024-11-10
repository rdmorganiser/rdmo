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

view_value_permission_map = {
    'owner': [1, 2, 3, 4, 5, 12],
    'manager': [1, 3, 5, 12],
    'author': [1, 3, 5, 12],
    'guest': [1, 3, 5, 12],
    'user': [12],
    'api': [1, 2, 3, 4, 5, 12],
    'site': [1, 2, 3, 4, 5, 12]
}

urlnames = {
    'list': 'v1-projects:value-list',
    'detail': 'v1-projects:value-detail',
    'file': 'v1-projects:value-file',
    'search': 'v1-projects:value-search'
}

values = [
    1, 2, 3, 4, 5, 6, 7, 238,  # from Test <1>
    242, 243,                  # from Parent <2>
    247,                       # from Child1 <3>
    248,                       # from Child2 <4>
    249,                       # from Child11 <5>
    456, 457                   # from Internal <12>
]
values_internal = [456]
values_snapshot_internal = [457]
snapshots = [1, 3, 7, 4, 5, 6, 8]
snapshots_internal = [8]

@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)

    if password:
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        if username == 'user':
            assert sorted([item['id'] for item in response.json()]) == values_internal
        else:
            values_list = Value.objects.filter(project__in=view_value_permission_map.get(username, [])) \
                                       .filter(snapshot_id=None) \
                                       .order_by('id').values_list('id', flat=True)
            assert sorted([item['id'] for item in response.json()]) == list(values_list)
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('snapshot_id', snapshots)
def test_list_snapshot(db, client, username, password, snapshot_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['list']) + f'?snapshot={snapshot_id}'
    response = client.get(url)

    if password:
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        if username == 'user':
            if snapshot_id in snapshots_internal:
                assert sorted([item['id'] for item in response.json()]) == values_snapshot_internal
            else:
                assert sorted([item['id'] for item in response.json()]) == []
        else:
            values_list = Value.objects.filter(project__in=view_value_permission_map.get(username, [])) \
                                       .filter(snapshot_id=snapshot_id) \
                                       .order_by('id').values_list('id', flat=True)
            assert sorted([item['id'] for item in response.json()]) == list(values_list)
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('value_id', values)
def test_detail(db, client, username, password, value_id):
    client.login(username=username, password=password)
    value = Value.objects.get(pk=value_id)

    url = reverse(urlnames['detail'], args=[value_id])
    response = client.get(url)

    if value.project.id in view_value_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') == value_id
    elif password:
        assert response.status_code == 404
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.post(url)

    if password:
        assert response.status_code == 405
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('value_id', values)
def test_update(db, client, username, password, value_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[value_id])
    data = {}
    response = client.put(url, data, content_type='application/json')

    if password:
        assert response.status_code == 405
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('value_id', values)
def test_delete(db, client, username, password, value_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[value_id])
    response = client.delete(url)

    if password:
        assert response.status_code == 405
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('value_id', values)
def test_file(db, client, files, username, password, value_id):
    client.login(username=username, password=password)
    value = Value.objects.get(pk=value_id)

    url = reverse(urlnames['file'], args=[value_id])
    response = client.get(url)

    if value.value_type == VALUE_TYPE_FILE and value.project.id in view_value_permission_map.get(username, []):
        assert response.status_code == 200
        assert response['Content-Type'] == value.file_type
        assert response['Content-Disposition'] == f'attachment; filename={value.file_name}'
        assert response.content == value.file.read()
    elif password:
        assert response.status_code == 404
    else:
        assert response.status_code == 401



@pytest.mark.parametrize('username,password', users)
def test_search(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['search'])
    response = client.get(url)

    if password:
        assert response.status_code == 200
        assert isinstance(response.json(), list)


        if username == 'user':
            assert sorted([item['id'] for item in response.json()]) == values_internal
        else:
            values_list = Value.objects.filter(project__in=view_value_permission_map.get(username, [])) \
                                       .filter(snapshot=None) \
                                       .exclude_empty()[:10]
            assert sorted([item['id'] for item in response.json()]) == sorted([item.id for item in values_list])
    else:
        assert response.status_code == 401
