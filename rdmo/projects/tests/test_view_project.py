import os
import re

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
    'update_get': {
        'owner': 200, 'manager': 200, 'author': 403, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'update_post': {
        'owner': 302, 'manager': 302, 'author': 403, 'guest': 403, 'user': 403, 'site': 302, 'anonymous': 302
    },
    'delete_get': {
        'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'delete_post': {
        'owner': 302, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'site': 302, 'anonymous': 302
    },
    'export': {
        'owner': 200, 'manager': 403, 'author': 403, 'guest': 403, 'user': 403, 'site': 200, 'anonymous': 302
    },
    'create_upload_get': {
        'owner': 302, 'manager': 302, 'author': 302, 'guest': 302, 'user': 302, 'site': 302, 'anonymous': 302
    },
    'create_upload_post': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'site': 200, 'anonymous': 302
    },
    'create_upload_post_error': {
        'owner': 400, 'manager': 400, 'author': 400, 'guest': 400, 'user': 400, 'site': 400, 'anonymous': 302
    },
    'create_upload_post_empty': {
        'owner': 302, 'manager': 302, 'author': 302, 'guest': 302, 'user': 302, 'site': 302, 'anonymous': 302
    },
    'create_import_get': {
        'owner': 302, 'manager': 302, 'author': 302, 'guest': 302, 'user': 302, 'site': 302, 'anonymous': 302
    },
    'create_import_post': {
        'owner': 302, 'manager': 302, 'author': 302, 'guest': 302, 'user': 302, 'site': 302, 'anonymous': 302
    },
    'create_import_post_error': {
        'owner': 400, 'manager': 400, 'author': 400, 'guest': 400, 'user': 400, 'site': 400, 'anonymous': 302
    },
    'create_import_post_empty': {
        'owner': 302, 'manager': 302, 'author': 302, 'guest': 302, 'user': 302, 'site': 302, 'anonymous': 302
    }
}

urlnames = {
    'list': 'projects',
    'site': 'site_projects',
    'detail': 'project',
    'create': 'project_create',
    'update': 'project_update',
    'delete': 'project_delete'
}


export_formats = ('rtf', 'odt', 'docx', 'html', 'markdown', 'tex', 'pdf')

site_id = 1
project_id = 1


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
def test_project_export_xml(db, client, username, password):
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
def test_project_create_upload_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_upload')
    response = client.get(url)
    assert response.status_code == status_map['create_upload_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_upload_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_upload')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})
    assert response.status_code == status_map['create_upload_post'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_upload_post_error(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_upload')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'error.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})
    assert response.status_code == status_map['create_upload_post_error'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_upload_post_empty(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_upload')
    response = client.post(url)
    assert response.status_code == status_map['create_upload_post_empty'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_import')
    response = client.get(url)
    assert response.status_code == status_map['create_import_get'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    # upload file
    url = reverse('project_create_upload')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})
    assert response.status_code == status_map['create_upload_post'][username], response.content

    # get uris from the response
    keys = re.findall(r'name=\"(.*?)\"', response.content.decode())

    # import file
    url = reverse('project_create_import')
    data = {key: ['on'] for key in keys}
    response = client.post(url, data)
    assert response.status_code == status_map['create_import_post'][username], response.content

    # assert that the project exists and that there are values
    if password:
        assert Project.objects.count() == 2
        assert Project.objects.order_by('updated').last().values.count() == 375
    else:
        assert Project.objects.count() == 1


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post_error(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_import')
    response = client.post(url)
    assert response.status_code == status_map['create_import_post_error'][username], response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post_empty(db, settings, client, username, password):
    client.login(username=username, password=password)

    # upload file
    url = reverse('project_create_upload')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})
    assert response.status_code == status_map['create_upload_post'][username], response.content

    url = reverse('project_create_import')
    response = client.post(url)
    assert response.status_code == status_map['create_import_post_empty'][username], response.content

    # assert that the project exists, but that there are not values
    if password:
        assert Project.objects.count() == 2
        assert Project.objects.order_by('updated').last().values.count() == 0
    else:
        assert Project.objects.count() == 1


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

    for view in views:
        url = reverse('project_view', args=[project_id, view.pk])
        response = client.get(url)

        status_code = status_map['detail'][username]
        if status_code not in [302, 403] and site_id not in view.sites.all():
            status_code = 404

        assert response.status_code == status_code, response.content


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('export_format', export_formats)
def test_project_view_export(db, client, username, password, export_format):
    client.login(username=username, password=password)
    views = View.objects.all()

    for view in views:
        url = reverse('project_view_export', args=[project_id, view.pk, export_format])
        response = client.get(url)

        status_code = status_map['detail'][username]
        if status_code not in [302, 403] and site_id not in view.sites.all():
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
