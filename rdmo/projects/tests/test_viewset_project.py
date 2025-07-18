import json
import xml.etree.ElementTree as et

import pytest

from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from django.urls import reverse

from ..models import Membership, Project, Snapshot, Value, Visibility

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('admin', 'admin'),
    ('api', 'api'),
    ('site', 'site'),
    ('user', 'user'),
    ('anonymous', None),
)

view_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10, 12],
    'manager': [1, 3, 5, 7, 12],
    'author': [1, 3, 5, 8, 12],
    'guest': [1, 3, 5, 9, 12],
    'admin': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'user': [12]
}

change_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10, 12],
    'manager': [1, 3, 5, 7],
    'admin': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
}

delete_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10, 12],
    'admin': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
}

urlnames = {
    "list": "v1-projects:project-list",
    "user": "v1-projects:project-user",
    "detail": "v1-projects:project-detail",
    "copy": "v1-projects:project-copy",
    "overview": "v1-projects:project-overview",
    "navigation": "v1-projects:project-navigation",
    "options": "v1-projects:project-options",
    "resolve": "v1-projects:project-resolve",
    "upload_accept": "v1-projects:project-upload-accept",
    "imports": "v1-projects:project-imports",
    "export": "v1-projects:project-export",
}

projects = [1, 2, 3, 4, 5, 12]
projects_visible = [12]
conditions = [1]

catalog_id = 1
catalog_id_not_available = 2

section_id = 1

optionset_id = 4

project_id = 1
parent_id = 3
parent_ancestors = [2, 3]

owner_id = 5
owner_projects = [1, 2, 3, 4, 5, 10, 12]

page_size = 5
export_formats = [None, 'xml','csvcomma', 'json']

@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)

    if password:
        response_data = response.json()

        assert response.status_code == 200
        assert isinstance(response_data, dict)

        if username == 'user':
            assert sorted([item['id'] for item in response.json().get('results')]) == projects_visible
        else:
            values_list = Project.objects.filter(id__in=view_project_permission_map.get(username, [])) \
                                         .values_list('id', flat=True)
            assert response_data['count'] == len(values_list)
            assert [item['id'] for item in response_data['results']] == list(values_list[:page_size])
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
def test_list_user(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list']) + f'?user={owner_id}'
    response = client.get(url)
    response_data = response.json()

    if password:
        assert response.status_code == 200
        assert isinstance(response_data, dict)

        if username == 'user':
            # only the visible project
            assert [item['id'] for item in response_data['results']] == [12]
        elif username in ['manager', 'author', 'guest']:
            # only memberships and visible
            assert [item['id'] for item in response_data['results']] == [1, 3, 5, 12]
        else:
            assert response_data['count'] == len(owner_projects)
            assert [item['id'] for item in response_data['results']] == list(owner_projects[:page_size])
    else:
        assert response.status_code == 401


def test_list_multisite(db, client, settings):
    settings.MULTISITE = True
    client.login(username='example-manager', password='example-manager')

    # create a project on site 2, which is visible on site 1
    project = Project.objects.create(title='foo.com project', site=Site.objects.get(id=2))
    visibility = Visibility.objects.create(project=project)
    visibility.sites.add(Site.objects.get(id=1))

    url = reverse(urlnames['list'])
    response = client.get(url + '?page=3')
    response_data = response.json()

    assert response.status_code == 200
    assert project.id in [i['id'] for i in response_data['results']]
    assert response_data['count'] == len(view_project_permission_map['site']) + 1


@pytest.mark.parametrize('username,password', users)
def test_user(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['user'])
    response = client.get(url)

    if password:
        response_data = response.json()

        assert response.status_code == 200
        assert isinstance(response_data, dict)

        if username in ['admin', 'site', 'api', 'user']:
            assert sorted([item['id'] for item in response.json().get('results')]) == projects_visible
        else:
            values_list = Project.objects.filter(id__in=view_project_permission_map.get(username, [])) \
                                         .values_list('id', flat=True)
            assert response_data['count'] == len(values_list)
            assert [item['id'] for item in response_data['results']] == list(values_list[:page_size])
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_detail(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[project_id])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') == project_id
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
def test_create(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    data = {
        'title': 'Lorem ipsum dolor sit amet',
        'description': 'At vero eos et accusam et justo duo dolores et ea rebum.',
        'catalog': catalog_id
    }
    response = client.post(url, data)

    if password:
        assert response.status_code == 201
        assert isinstance(response.json(), dict)
        assert Project.objects.get(id=response.json().get('id'))
    else:
        assert response.status_code == 401


def test_create_restricted(db, client, settings):
    settings.PROJECT_CREATE_RESTRICTED = True
    settings.PROJECT_CREATE_GROUPS = ['projects']

    group = Group.objects.create(name='projects')
    user = User.objects.get(username='user')
    user.groups.add(group)

    client.login(username='user', password='user')

    url = reverse(urlnames['list'])
    data = {
        'title': 'Lorem ipsum dolor sit amet',
        'description': 'At vero eos et accusam et justo duo dolores et ea rebum.',
        'catalog': catalog_id
    }
    response = client.post(url, data)

    assert response.status_code == 201


def test_create_forbidden(db, client, settings):
    settings.PROJECT_CREATE_RESTRICTED = True

    client.login(username='user', password='user')

    url = reverse(urlnames['list'])
    data = {
        'title': 'Lorem ipsum dolor sit amet',
        'description': 'At vero eos et accusam et justo duo dolores et ea rebum.',
        'catalog': catalog_id
    }
    response = client.post(url, data)

    assert response.status_code == 403


def test_create_catalog_missing(db, client):
    client.login(username='user', password='user')

    url = reverse(urlnames['list'])
    data = {
        'title': 'Lorem ipsum dolor sit amet',
        'description': 'At vero eos et accusam et justo duo dolores et ea rebum.'
    }
    response = client.post(url, data)

    assert response.status_code == 400


def test_create_catalog_not_available(db, client):
    client.login(username='user', password='user')

    url = reverse(urlnames['list'])
    data = {
        'title': 'Lorem ipsum dolor sit amet',
        'description': 'At vero eos et accusam et justo duo dolores et ea rebum.',
        'catalog': catalog_id_not_available
    }
    response = client.post(url, data)

    assert response.status_code == 400


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_create_parent(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    data = {
        'title': 'Lorem ipsum dolor sit amet',
        'description': 'At vero eos et accusam et justo duo dolores et ea rebum.',
        'catalog': catalog_id,
        'parent': project_id
    }
    response = client.post(url, data)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 201
        assert isinstance(response.json(), dict)
        assert Project.objects.get(id=response.json().get('id'))
    else:
        if password:
            assert response.status_code == 400
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_copy(db, files, client, username, password, project_id):
    client.login(username=username, password=password)

    project_count = Project.objects.count()
    snapshot_count = Snapshot.objects.count()
    value_count = Value.objects.count()

    project = Project.objects.get(id=project_id)
    project_snapshots_count = project.snapshots.count()
    project_values_count = project.values.count()

    url = reverse(urlnames['copy'], args=[project_id])
    data = {
        'title': 'New title',
        'description': project.description,
        'catalog': project.catalog.id
    }
    response = client.post(url, data, content_type='application/json')

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 201

        for key, value in response.json().items():
            if key in data:
                assert value == data[key]

        assert Project.objects.count() == project_count + 1
        assert Snapshot.objects.count() == snapshot_count + project_snapshots_count
        assert Value.objects.count() == value_count + project_values_count
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401

        assert Project.objects.count() == project_count
        assert Value.objects.count() == value_count


def test_copy_restricted(db, files, client, settings):
    settings.PROJECT_CREATE_RESTRICTED = True
    settings.PROJECT_CREATE_GROUPS = ['projects']

    group = Group.objects.create(name='projects')
    user = User.objects.get(username='user')
    user.groups.add(group)

    Membership.objects.create(user=user, project_id=project_id, role='guest')

    client.login(username='user', password='user')

    url = reverse(urlnames['copy'], args=[project_id])
    data = {
        'title': 'Lorem ipsum dolor sit amet',
        'description': 'At vero eos et accusam et justo duo dolores et ea rebum.',
        'catalog': catalog_id
    }
    response = client.post(url, data, content_type='application/json')

    assert response.status_code == 201


def test_copy_forbidden(db, client, settings):
    settings.PROJECT_CREATE_RESTRICTED = True

    user = User.objects.get(username='user')

    Membership.objects.create(user=user, project_id=project_id, role='guest')

    client.login(username='user', password='user')

    url = reverse(urlnames['copy'], args=[project_id])
    data = {
        'title': 'Lorem ipsum dolor sit amet',
        'description': 'At vero eos et accusam et justo duo dolores et ea rebum.',
        'catalog': catalog_id
    }
    response = client.post(url, data)

    assert response.status_code == 403


def test_copy_catalog_missing(db, client):
    client.login(username='guest', password='guest')

    url = reverse(urlnames['copy'], args=[project_id])
    data = {
        'title': 'Lorem ipsum dolor sit amet',
        'description': 'At vero eos et accusam et justo duo dolores et ea rebum.'
    }
    response = client.post(url, data)

    assert response.status_code == 400


def test_copy_catalog_not_available(db, client):
    client.login(username='guest', password='guest')

    url = reverse(urlnames['copy'], args=[project_id])
    data = {
        'title': 'Lorem ipsum dolor sit amet',
        'description': 'At vero eos et accusam et justo duo dolores et ea rebum.',
        'catalog': catalog_id_not_available
    }
    response = client.post(url, data)

    assert response.status_code == 400

@pytest.mark.parametrize('project_id', projects)
def test_copy_parent(db, files, client, project_id):
    client.login(username='owner', password='owner')
    project = Project.objects.get(pk=project_id)

    url = reverse(urlnames['copy'], args=[project_id])
    data = {
        'title': 'New title',
        'description': project.description,
        'catalog': project.catalog.id,
        'parent': parent_id
    }
    response = client.post(url, data, content_type='application/json')

    assert response.status_code == 201


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_update(db, client, username, password, project_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)

    url = reverse(urlnames['detail'], args=[project_id])
    data = {
        'title': 'New title',
        'description': project.description,
        'catalog': project.catalog.id
    }
    response = client.put(url, data, content_type='application/json')

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert Project.objects.get(id=project_id).title == 'New title'
        assert Project.objects.get(id=project_id).description == project.description
    else:
        if project_id in view_project_permission_map.get(username, []):
            assert response.status_code == 403
        elif password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401

        assert Project.objects.get(id=project_id).title == project.title
        assert Project.objects.get(id=project_id).description == project.description


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_update_parent(db, client, username, password, project_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)

    url = reverse(urlnames['detail'], args=[project_id])
    data = {
        'title': 'New title',
        'description': project.description,
        'catalog': project.catalog.id,
        'parent': parent_id
    }
    response = client.put(url, data, content_type='application/json')

    if project_id in change_project_permission_map.get(username, []):
        if parent_id in view_project_permission_map.get(username, []):
            if project_id in parent_ancestors:
                assert response.status_code == 400
                assert Project.objects.get(pk=project_id).parent == project.parent
            else:
                assert response.status_code == 200
                assert Project.objects.get(pk=project_id).parent_id == parent_id
        else:
            assert response.status_code == 404
            assert Project.objects.get(pk=project_id).parent == project.parent
    else:
        if project_id in view_project_permission_map.get(username, []):
            assert response.status_code == 403
        elif password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401

        assert Project.objects.get(pk=project_id).parent == project.parent


def test_update_project_views_not_allowed(db, client, settings, enable_project_views_sync):
    assert settings.PROJECT_VIEWS_SYNC

    client.login(username='owner', password='owner')
    url = reverse(urlnames['detail'], args=[project_id])
    data = {
        'views': [1]
    }
    response = client.put(url, data, content_type='application/json')

    assert response.status_code == 400
    assert 'Editing views is disabled' in ' '.join(response.json()['views'])


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_delete(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[project_id])
    response = client.delete(url)

    if project_id in delete_project_permission_map.get(username, []):
        assert response.status_code == 204
        assert Project.objects.filter(id=project_id).first() is None
    else:
        if project_id in view_project_permission_map.get(username, []):
            assert response.status_code == 403
        elif password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401

        assert Project.objects.filter(id=project_id).first()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('condition_id', conditions)
def test_overview(db, client, username, password, project_id, condition_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['overview'], args=[project_id])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') == project_id
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_navigation(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['navigation'], args=[project_id])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_navigation_section(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['navigation'], args=[project_id]) + f'{section_id}/'
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('condition_id', conditions)
def test_resolve(db, client, username, password, project_id, condition_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['resolve'], args=[project_id]) + f'?condition={condition_id}'
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
def test_options(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['options'], args=[project_id]) + f'?optionset={optionset_id}'
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        for item in response.json():
            assert item['text_and_help'] == '{text} [{help}]'.format(**item)
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


def test_options_text_and_help(db, client, mocker):
    mocker.patch('rdmo.options.providers.SimpleProvider.get_options', return_value=[
        {
            'id': 'simple_1',
            'text': 'Simple answer 1'
        }
    ])

    client.login(username='author', password='author')

    url = reverse(urlnames['options'], args=[project_id]) + f'?optionset={optionset_id}'
    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == [
        {
            'id': 'simple_1',
            'text': 'Simple answer 1',
            'text_and_help': 'Simple answer 1'
        }
    ]


@pytest.mark.parametrize('username,password', users)
def test_upload_accept(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['upload_accept'])
    response = client.get(url)

    if password:
        assert response.status_code == 200
        assert response.json() == {
            'application/xml': ['.xml']
        }
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
def test_imports(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['imports'])
    response = client.get(url)

    if password:
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]['key'] == 'url'
    else:
        assert response.status_code == 401

@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_export(db, client, username, password, export_format):
    client.login(username=username, password=password)

    if export_format:
        url = reverse(urlnames["export"], kwargs={"pk": project_id, "export_format": export_format})
    else:
        url = reverse(urlnames["export"], kwargs={"pk": project_id})

    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
        assert response.content

        # XML (default or explicit)
        if export_format in (None, "xml"):
            root = et.fromstring(response.content)
            assert root.tag == "project"
            for child in root:
                assert child.tag in ['title', 'description', 'catalog', 'tasks', 'views',
                                     'snapshots', 'values', 'created', 'updated']

        # JSON
        elif export_format == "json":
            data = json.loads(response.content.decode())
            assert len(data) > 1
            assert all(
                all(
                    a in ['question','set', 'values']
                    for a in i.keys()
                )
               for i in data
            )

        # HTML (or any other plugin-provided format)
        elif export_format == "csvcomma":
            data = response.content.decode().splitlines()
            assert len(data) > 1
            assert any("Lorem" in i for i in data)
    else:
        if password:
            # you have permission to see detail but not export
            assert response.status_code in (403, 404)
        else:
            assert response.status_code == 401
