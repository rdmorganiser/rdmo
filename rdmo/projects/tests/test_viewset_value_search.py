import pytest

from django.urls import reverse

from ..models import Value

view_value_permission_map = {
    'owner': [1, 2, 3, 4, 5, 12],
}

urlnames = {
    'search': 'v1-projects:value-search'
}

attribute_id = 14
search = 'Fir'
options = [1, 2, 3]

def test_search(db, client):
    client.login(username='owner', password='owner')

    url = reverse(urlnames['search'])
    response = client.get(url)

    values_list = Value.objects.filter(project__in=view_value_permission_map.get('owner', [])) \
                               .filter(snapshot=None) \
                               .exclude_empty().order_by(*Value._meta.ordering)[:10]
    assert sorted([item['id'] for item in response.json()]) == sorted([item.id for item in values_list])


def test_search_options(db, client):
    client.login(username='owner', password='owner')

    url = reverse(urlnames['search']) + '?' + '&'.join([f'option={o}' for o in options])
    response = client.get(url)

    values_list = Value.objects.filter(project__in=view_value_permission_map.get('owner', [])) \
                               .filter(snapshot=None, option__in=options) \
                               .exclude_empty()[:10]

    assert sorted([item['id'] for item in response.json()]) == sorted([item.id for item in values_list])


def test_search_no_options(db, client):
    client.login(username='owner', password='owner')

    url = reverse(urlnames['search']) + '?option='
    response = client.get(url)

    values_list = Value.objects.filter(project__in=view_value_permission_map.get('owner', [])) \
                               .filter(snapshot=None, option=None) \
                               .exclude_empty()[:10]

    assert sorted([item['id'] for item in response.json()]) == sorted([item.id for item in values_list])


def test_search_attribute(db, client):
    client.login(username='owner', password='owner')

    url = reverse(urlnames['search']) + f'?attribute={attribute_id}'
    response = client.get(url)

    values_list = Value.objects.filter(project__in=view_value_permission_map.get('owner', [])) \
                               .filter(attribute_id=attribute_id, snapshot=None) \
                               .exclude_empty()[:10]
    assert sorted([item['id'] for item in response.json()]) == sorted([item.id for item in values_list])


def test_search_attribute_snapshot(db, client):
    client.login(username='owner', password='owner')

    url = reverse(urlnames['search']) + f'?attribute={attribute_id}&snapshot=all'
    response = client.get(url)

    values_list = Value.objects.filter(project__in=view_value_permission_map.get('owner', [])) \
                               .filter(attribute_id=attribute_id) \
                               .exclude_empty()[:10]
    assert sorted([item['id'] for item in response.json()]) == sorted([item.id for item in values_list])

@pytest.mark.parametrize('collection', ["true", "false"])
def test_search_attribute_search_collection(db, client, collection):
    client.login(username='owner', password='owner')

    url = reverse(urlnames['search']) + f'?attribute={attribute_id}&collection={collection}&search={search}'
    response = client.get(url)

    values_list = Value.objects.filter(project__in=view_value_permission_map.get('owner', [])) \
                               .filter(attribute_id=attribute_id, text__contains=search) \
                               .exclude_empty()[:10]
    assert sorted([item['id'] for item in response.json()]) == sorted([item.id for item in values_list])
