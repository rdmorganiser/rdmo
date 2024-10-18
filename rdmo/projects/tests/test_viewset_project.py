import pytest

from django.contrib.auth.models import Group, User
from django.urls import reverse

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

view_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10],
    'manager': [1, 3, 5, 7],
    'author': [1, 3, 5, 8],
    'guest': [1, 3, 5, 9],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
}

change_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10],
    'manager': [1, 3, 5, 7],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}

delete_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}

urlnames = {
    'list': 'v1-projects:project-list',
    'detail': 'v1-projects:project-detail',
    'overview': 'v1-projects:project-overview',
    'navigation': 'v1-projects:project-navigation',
    'options': 'v1-projects:project-options',
    'resolve': 'v1-projects:project-resolve',
    'upload_accept': 'v1-projects:project-upload-accept',
    'imports': 'v1-projects:project-imports'
}

projects = [1, 2, 3, 4, 5]
conditions = [1]

catalog_id = 1
catalog_id_not_available = 2

section_id = 1

optionset_id = 4

project_id = 1

page_size = 5

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
            assert response_data['count'] == 0
            assert response_data['results'] == []
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
@pytest.mark.parametrize('condition_id', conditions)
def test_navigation(db, client, username, password, project_id, condition_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['navigation'], args=[project_id, section_id])
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
            'application/xml': ['.xml'],
            'text/xml': ['.xml']
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
