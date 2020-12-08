import pytest
from django.urls import reverse

from rdmo.views.models import View

from ..models import Project

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

status_map = {
    'list': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'site': 200, 'anonymous': 302,
    },
    'site': {
        'owner': 403, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302,
    },
    'detail': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'create_get': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'site': 200, 'anonymous': 302
    },
    'create_post': {
        'owner': 302, 'manager': 302, 'author': 302, 'guest': 302, 'user': 302, 'site': 302, 'anonymous': 302
    },
    'create_post_parent': {
        'owner': 302, 'manager': 302, 'author': 302, 'guest': 302, 'user': 200, 'site': 302, 'anonymous': 302
    },
    'update_get': {
        'owner': 200, 'manager': 200, 'author': 403, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'update_post': {
        'owner': 302, 'manager': 302, 'author': 403, 'guest': 403, 'user': 403, 'site': 302, 'anonymous': 302
    },
    'update_parent_post': {
        'owner': 302, 'manager': 200, 'author': 403, 'guest': 403, 'user': 403, 'site': 302, 'anonymous': 302
    },
    'delete_get': {
        'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'delete_post': {
        'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'site': 302, 'anonymous': 302
    },
    'export': {
        'owner': 200, 'manager': 200, 'author': 403, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302
    }
}

urlnames = {
    'list': 'projects',
    'site': 'site_projects',
    'detail': 'project',
    'create': 'project_create',
    'update': 'project_update',
    'update_information': 'project_update_information',
    'update_catalog': 'project_update_catalog',
    'update_tasks': 'project_update_tasks',
    'update_views': 'project_update_views',
    'update_parent': 'project_update_parent',
    'delete': 'project_delete'
}


export_formats = ('rtf', 'odt', 'docx', 'html', 'markdown', 'tex', 'pdf')

site_id = 1
project_id = 1
catalog_id = 1


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_site(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['site'])
    response = client.get(url)
    assert response.status_code == status_map['site'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_detail(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['create'])
    response = client.get(url)
    assert response.status_code == status_map['create_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_post(db, client, username, password):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)

    url = reverse(urlnames['create'])
    data = {
        'title': 'A new project',
        'description': 'Some description',
        'catalog': project.catalog.pk
    }
    response = client.post(url, data)
    assert response.status_code == status_map['create_post'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_parent_post(db, client, username, password):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)

    url = reverse(urlnames['create'])
    data = {
        'title': 'A new project',
        'description': 'Some description',
        'catalog': project.catalog.pk,
        'parent': project_id
    }
    response = client.post(url, data)
    assert response.status_code == status_map['create_post_parent'][username], response.content
    if response.status_code == 302 and password:
        assert Project.objects.order_by('-created').first().parent_id == project_id


@pytest.mark.parametrize('username,password', users)
def test_project_update_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update'], args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['update_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_post(db, client, username, password):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)

    url = reverse(urlnames['update'], args=[project_id])
    data = {
        'title': project.title,
        'description': project.description,
        'catalog': project.catalog.pk
    }
    response = client.post(url, data)
    assert response.status_code == status_map['update_post'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_post_parent(db, client, username, password):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)
    parent = Project.objects.get(title='Parent')

    url = reverse(urlnames['update'], args=[project_id])
    data = {
        'title': project.title,
        'description': project.description,
        'catalog': project.catalog.pk,
        'parent': parent.id
    }
    response = client.post(url, data)
    assert response.status_code == status_map['update_parent_post'][username], response.content
    if response.status_code == 302 and password:
        assert Project.objects.get(pk=project_id).parent == parent
    else:
        assert Project.objects.get(pk=project_id).parent == project.parent


@pytest.mark.parametrize('username,password', users)
def test_project_update_information_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update'], args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['update_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_information_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update_information'], args=[project_id])
    data = {
        'title': 'Lorem ipsum dolor sit amet',
        'description': 'At vero eos et accusam et justo duo dolores et ea rebum.'
    }
    response = client.post(url, data)
    assert response.status_code == status_map['update_post'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_catalog_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update_catalog'], args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['update_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_catalog_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update_catalog'], args=[project_id])
    data = {
        'catalog': catalog_id
    }
    response = client.post(url, data)
    assert response.status_code == status_map['update_post'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_tasks_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update_tasks'], args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['update_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_tasks_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update_tasks'], args=[project_id])
    data = {
        'tasks': []
    }
    response = client.post(url, data)
    assert response.status_code == status_map['update_post'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_views_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update_views'], args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['update_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_views_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update_views'], args=[project_id])
    data = {
        'views': []
    }
    response = client.post(url, data)
    assert response.status_code == status_map['update_post'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_parent_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['update_parent'], args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['update_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_parent_post(db, client, username, password):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)
    parent = Project.objects.get(title='Parent')

    url = reverse(urlnames['update_parent'], args=[project_id])
    data = {
        'parent': parent.id
    }
    response = client.post(url, data)
    assert response.status_code == status_map['update_parent_post'][username], response.content
    if response.status_code == 302 and password:
        assert Project.objects.get(pk=project_id).parent == parent
    else:
        assert Project.objects.get(pk=project_id).parent == project.parent


@pytest.mark.parametrize('username,password', users)
def test_project_delete_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['delete'], args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['delete_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_delete_update_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['delete'], args=[project_id])
    response = client.post(url)
    assert response.status_code == status_map['delete_post'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_export_xml(db, client, files, username, password):
    client.login(username=username, password=password)

    url = reverse('project_export', args=[project_id, 'xml'])
    response = client.get(url)
    assert response.status_code == status_map['export'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_export_csv(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_export', args=[project_id, 'csvcomma'])
    response = client.get(url)
    assert response.status_code == status_map['export'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_export_csvsemicolon(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_export', args=[project_id, 'csvsemicolon'])
    response = client.get(url)
    assert response.status_code == status_map['export'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_answers(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_answers', args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_project_answers_export(db, client, username, password, export_format):
    client.login(username=username, password=password)

    url = reverse('project_answers_export', args=[project_id, export_format])
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_view(db, client, username, password):
    client.login(username=username, password=password)
    views = View.objects.all()
    project_views = Project.objects.get(pk=project_id).views.all()

    for view in views:
        url = reverse('project_view', args=[project_id, view.pk])
        response = client.get(url)

        if view in project_views:
            status_code = status_map['detail'][username]
        else:
            status_code = 404

        assert response.status_code == status_code, response.content


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_project_view_export(db, client, username, password, export_format):
    client.login(username=username, password=password)
    views = View.objects.all()
    project_views = Project.objects.get(pk=project_id).views.all()

    for view in views:
        url = reverse('project_view_export', args=[project_id, view.pk, export_format])
        response = client.get(url)

        if view in project_views:
            status_code = status_map['detail'][username]
        else:
            status_code = 404

        assert response.status_code == status_code, response.content


@pytest.mark.parametrize('username,password', users)
def test_project_questions(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_questions', args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_error(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_error', args=[project_id])
    response = client.get(url)
    assert response.status_code == status_map['detail'][username], response.content
