import xml.etree.ElementTree as et

import itertools
import pytest
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.urls import reverse

from rdmo.projects.models import Project
from rdmo.questions.models import Catalog

from ..models import View

users = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('api', 'api'),
    ('anonymous', None),
)

view_project_test_users = (
    ('editor', 'editor'),
    ('api', 'api'),
)


status_map = {
    'list': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 401
    },
    'detail': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 401
    },
    'create': {
        'editor': 201, 'reviewer': 403, 'api': 201, 'user': 403, 'anonymous': 401
    },
    'update': {
        'editor': 200, 'reviewer': 403, 'api': 200, 'user': 403, 'anonymous': 401
    },
    'delete': {
        'editor': 204, 'reviewer': 403, 'api': 204, 'user': 403, 'anonymous': 401
    }
}

urlnames = {
    'list': 'v1-views:view-list',
    'index': 'v1-views:view-index',
    'export': 'v1-views:view-export',
    'detail': 'v1-views:view-detail',
    'detail_export': 'v1-views:view-detail-export',
    'copy': 'v1-views:view-copy'
}

view_update_tests = [
    # tuples of: view_id, sites, catalogs, groups, project_id, project_exists
    ('3', [],       [],     [], '10', True),
    ('3', [2],      [],     [], '10', False),
    ('3', [1,2,3],  [],     [], '10', True),
    ('3', [],       [2],    [], '10', False),
    ('3', [2],      [2],    [], '10', False),
    ('3', [1,2,3],  [2],    [], '10', False),
    ('3', [],       [1,2],  [], '10', True),
    ('3', [2],      [1,2],  [], '10', False),
    ('3', [1,2,3],  [1,2],  [], '10', True),

    ('3', [],       [],     [1], '10', False),
    ('3', [2],      [],     [1], '10', False),
    ('3', [1,2,3],  [],     [1], '10', False),
    ('3', [],       [2],    [1], '10', False),
    ('3', [2],      [2],    [1], '10', False),
    ('3', [1,2,3],  [2],    [1], '10', False),
    ('3', [],       [1,2],  [1], '10', False),
    ('3', [2],      [1,2],  [1], '10', False),
    ('3', [1,2,3],  [1,2],  [1], '10', False),

    ('3', [],       [],     [1,2,3,4], '10', True),
    ('3', [2],      [],     [1,2,3,4], '10', False),
    ('3', [1,2,3],  [],     [1,2,3,4], '10', True),
    ('3', [],       [2],    [1,2,3,4], '10', False),
    ('3', [2],      [2],    [1,2,3,4], '10', False),
    ('3', [1,2,3],  [2],    [1,2,3,4], '10', False),
    ('3', [],       [1,2],  [1,2,3,4], '10', True),
    ('3', [2],      [1,2],  [1,2,3,4], '10', False),
    ('3', [1,2,3],  [1,2],  [1,2,3,4], '10', True)
]

@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_index(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['index'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_export(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['export'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.content

    if response.status_code == 200:
        root = et.fromstring(response.content)
        assert root.tag == 'rdmo'
        for child in root:
            assert child.tag in ['view']


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)
    instances = View.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['detail'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)
    instances = View.objects.all()

    for instance in instances:
        url = reverse(urlnames['list'])
        data = {
            'uri_prefix': instance.uri_prefix,
            'key': '%s_new_%s' % (instance.key, username),
            'comment': instance.comment,
            'template': instance.template,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'help_en': instance.help_lang1,
            'help_de': instance.help_lang2
        }
        response = client.post(url, data)
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_update(db, client, username, password):
    client.login(username=username, password=password)
    instances = View.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix,
            'key': instance.key,
            'comment': instance.comment,
            'template': instance.template,
            'title_en': instance.title_lang1,
            'title_de': instance.title_lang2,
            'help_en': instance.help_lang1,
            'help_de': instance.help_lang2
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['update'][username], response.json()

@pytest.mark.parametrize('view_id,sites,catalogs,groups,project_id,project_exists', view_update_tests)
def test_update_projects(db, view_id, sites, catalogs, groups, project_id, project_exists):
    view = View.objects.get(pk=view_id)
    project = Project.objects.get(pk=project_id)

    view.sites.set(Site.objects.filter(pk__in=sites))
    view.catalogs.set(Catalog.objects.filter(pk__in=catalogs))
    view.groups.set(Group.objects.filter(pk__in=groups))

    assert sorted(list(itertools.chain.from_iterable(view.sites.all().values_list('pk')))) == sites
    assert sorted(list(itertools.chain.from_iterable(view.catalogs.all().values_list('pk')))) == catalogs
    assert sorted(list(itertools.chain.from_iterable(view.groups.all().values_list('pk')))) == groups

    if not project_exists:
        with pytest.raises(Project.DoesNotExist):
            Project.objects.filter(views=view).get(pk=project_id)
    else:
        assert Project.objects.filter(views=view).get(pk=project_id)

@pytest.mark.parametrize('username,password', users)
def test_delete(db, client, username, password):
    client.login(username=username, password=password)
    instances = View.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail'], args=[instance.pk])
        response = client.delete(url)
        assert response.status_code == status_map['delete'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_detail_export(db, client, username, password):
    client.login(username=username, password=password)
    instances = View.objects.all()

    for instance in instances:
        url = reverse(urlnames['detail_export'], args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status_map['list'][username], response.content

        if response.status_code == 200:
            root = et.fromstring(response.content)
            assert root.tag == 'rdmo'
            for child in root:
                assert child.tag in ['view']


@pytest.mark.parametrize('username,password', users)
def test_copy(db, client, username, password):
    client.login(username=username, password=password)
    instances = View.objects.all()

    for instance in instances:
        url = reverse(urlnames['copy'], args=[instance.pk])
        data = {
            'uri_prefix': instance.uri_prefix + '-',
            'key': instance.key + '-'
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status_map['create'][username], response.json()


@pytest.mark.parametrize('username,password', users)
def test_copy_wrong(db, client, username, password):
    client.login(username=username, password=password)
    instance = View.objects.first()

    url = reverse(urlnames['copy'], args=[instance.pk])
    data = {
        'uri_prefix': instance.uri_prefix,
        'key': instance.key
    }
    response = client.put(url, data, content_type='application/json')

    if status_map['create'][username] == 201:
        assert response.status_code == 400, response.json()
    else:
        assert response.status_code == status_map['create'][username], response.json()
