import xml.etree.ElementTree as et

import pytest

from django.urls import reverse

from ..models import Snapshot

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

view_snapshot_permission_map = {
    'owner': [1, 2, 3, 4, 5, 12],
    'manager': [1, 3, 5, 12],
    'author': [1, 3, 5, 12],
    'guest': [1, 3, 5, 12],
    'user': [12],
    'api': [1, 2, 3, 4, 5, 12],
    'site': [
        1, 2, 3, 4, 5, 12]
}

urlnames = {
    'list': 'v1-projects:snapshot-list',
    'detail': 'v1-projects:snapshot-detail',
    'export': 'v1-projects:project-snapshot-export',
}

snapshots = [
    1, 7,  # from Test <1>
    3,     # from Parent <2>
    4,     # from Child1 <3>
    5,     # from Child2 <4>
    6,     # from Child11 <5>
    8      # from Internal <12>
]
snapshots_visible = [8]


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)

    if password:
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        if username == 'user':
            assert sorted([item['id'] for item in response.json()]) == snapshots_visible
        else:
            values_list = Snapshot.objects.filter(project__in=view_snapshot_permission_map.get(username, [])) \
                                          .order_by('id').values_list('id', flat=True)
            assert sorted([item['id'] for item in response.json()]) == list(values_list)
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('snapshot_id', snapshots)
def test_detail(db, client, username, password, snapshot_id):
    client.login(username=username, password=password)
    snapshot = Snapshot.objects.get(id=snapshot_id)

    url = reverse(urlnames['detail'], args=[snapshot_id])
    response = client.get(url)

    if snapshot.project.id in view_snapshot_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') == snapshot_id
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
@pytest.mark.parametrize('snapshot_id', snapshots)
def test_update(db, client, username, password, snapshot_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[snapshot_id])
    response = client.put(url, content_type='application/json')

    if password:
        assert response.status_code == 405
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('snapshot_id', snapshots)
def test_delete(db, client, username, password, snapshot_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[snapshot_id])
    response = client.delete(url)

    if password:
        assert response.status_code == 405
    else:
        assert response.status_code == 401



@pytest.mark.parametrize("username,password", users)
@pytest.mark.parametrize("include_memberships", [False, True])
def test_export(db, client, username, password, include_memberships):
    snapshot_id = 1
    client.login(username=username, password=password)

    snapshot = Snapshot.objects.get(pk=snapshot_id)

    url = reverse(
        urlnames["export"],
        kwargs={
            "parent_lookup_project": snapshot.project_id,
            "pk": snapshot.pk,
        },
    )

    if include_memberships:
        url += "?include_memberships=1"

    response = client.get(url)

    if snapshot.project.id in view_snapshot_permission_map.get(username, []):
        assert response.status_code == 200
        assert response.content

        root = et.fromstring(response.content)
        assert root.tag == "project"

        expected_tags = [
            "title", "description", "catalog", "tasks", "views",
            "snapshots", "values", "memberships", "created", "updated"
        ]

        for child in root:
            assert child.tag in expected_tags

        memberships_el = root.find("memberships")
        if include_memberships:
            assert memberships_el is not None
            assert len(list(memberships_el)) > 0
        else:
            if memberships_el is None:
                pass
            else:
                assert len(list(memberships_el)) == 0

    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 404
