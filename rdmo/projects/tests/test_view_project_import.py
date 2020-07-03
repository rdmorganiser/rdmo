import os
import re
from datetime import timedelta

import pytest

from django.urls import reverse
from django.utils import timezone

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
    'create_upload_get': {
        'owner': 302, 'manager': 302, 'author': 302, 'guest': 302, 'user': 302, 'site': 302
    },
    'create_upload_post': {
        'owner': 200, 'manager': 200, 'author': 200, 'guest': 200, 'user': 200, 'site': 200
    },
    'create_upload_error': {
        'owner': 400, 'manager': 400, 'author': 400, 'guest': 400, 'user': 400, 'site': 400
    },
    'create_upload_empty': {
        'owner': 302, 'manager': 302, 'author': 302, 'guest': 302, 'user': 302, 'site': 302
    },
    'create_import_get': {
        'owner': 302, 'manager': 302, 'author': 302, 'guest': 302, 'user': 302, 'site': 302
    },
    'create_import_post': {
        'owner': 302, 'manager': 302, 'author': 302, 'guest': 302, 'user': 302, 'site': 302
    },
    'create_import_error': {
        'owner': 400, 'manager': 400, 'author': 400, 'guest': 400, 'user': 400, 'site': 400
    },
    'create_import_empty': {
        'owner': 302, 'manager': 302, 'author': 302, 'guest': 302, 'user': 302, 'site': 302
    },
    'update_upload_get': {
        'owner': 302, 'manager': 302, 'author': 403, 'guest': 403, 'user': 403, 'site': 302
    },
    'update_upload_post': {
        'owner': 200, 'manager': 200, 'author': 403, 'guest': 403, 'user': 403, 'site': 200
    },
    'update_upload_error': {
        'owner': 400, 'manager': 400, 'author': 403, 'guest': 403, 'user': 403, 'site': 400
    },
    'update_upload_empty': {
        'owner': 302, 'manager': 302, 'author': 403, 'guest': 403, 'user': 403, 'site': 302
    },
    'update_import_get': {
        'owner': 302, 'manager': 302, 'author': 403, 'guest': 403, 'user': 403, 'site': 302
    },
    'update_import_post': {
        'owner': 302, 'manager': 302, 'author': 403, 'guest': 403, 'user': 403, 'site': 302
    },
    'update_import_error': {
        'owner': 400, 'manager': 400, 'author': 403, 'guest': 403, 'user': 403, 'site': 400
    },
    'update_import_empty': {
        'owner': 302, 'manager': 302, 'author': 403, 'guest': 403, 'user': 403, 'site': 302
    }
}

project_id = 1


@pytest.mark.parametrize('username,password', users)
def test_project_create_upload_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_upload')
    response = client.get(url)
    if password:
        assert response.status_code == status_map['create_upload_get'][username], response.content
        if response.status_code == 302:
            assert response.url == '/projects/', response.content
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_upload_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_upload')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if password:
        assert response.status_code == status_map['create_upload_post'][username], response.content
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_upload_post_error(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_upload')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'error.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if password:
        assert response.status_code == status_map['create_upload_error'][username], response.content
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_upload_post_empty(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_upload')
    response = client.post(url)
    if password:
        assert response.status_code == status_map['create_upload_empty'][username], response.content
        if response.status_code == 302:
            assert response.url == '/projects/'
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_import')
    response = client.get(url)
    if password:
        assert response.status_code == status_map['create_import_get'][username], response.content
        if response.status_code == 302:
            assert response.url == '/projects/'
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    # upload file
    url = reverse('project_create_upload')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if password:
        assert response.status_code == status_map['create_upload_post'][username], response.content

        # get keys from the response
        keys = re.findall(r'name=\"(.*?)\"', response.content.decode())

        # import file
        url = reverse('project_create_import')
        data = {key: ['on'] for key in keys}
        response = client.post(url, data)

        # assert that the project exists and that there are values
        if password:
            project = Project.objects.order_by('updated').last()
            assert response.status_code == status_map['create_import_post'][username], response.content
            if response.status_code == 302:
                assert response.url == '/projects/{}/'.format(project.pk)

                # a new project, new values values
                assert Project.objects.count() == 2
                assert project.values.count() == 225
        else:
            assert response.status_code == 302, response.content
            assert response.url.startswith('/account/login/'), response.content

            # no new project was created
            assert Project.objects.count() == 1
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post_error(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create_import')
    response = client.post(url)
    if password:
        assert response.status_code == status_map['create_import_error'][username], response.content
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_create_import_post_empty(db, settings, client, username, password):
    client.login(username=username, password=password)

    # upload file
    url = reverse('project_create_upload')
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if password:
        assert response.status_code == status_map['create_upload_post'][username], response.content

        url = reverse('project_create_import')
        response = client.post(url)

        # assert that the project exists, but that there are not values
        if password:
            project = Project.objects.order_by('updated').last()
            assert response.status_code == status_map['create_import_empty'][username], response.content
            if response.status_code == 302:
                assert response.url == '/projects/{}/'.format(project.pk)

                # a new project, but no values
                assert Project.objects.count() == 2
                assert project.values.count() == 0
        else:
            assert response.status_code == 302, response.content
            assert response.url.startswith('/account/login/'), response.content

            # no new project was created
            assert Project.objects.count() == 1
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_upload_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_update_upload', args=[project_id])
    response = client.get(url)
    if password:
        assert response.status_code == status_map['update_upload_get'][username], response.content
        if response.status_code == 302:
            assert response.url == '/projects/{}/'.format(project_id), response.content
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_upload_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_update_upload', args=[project_id])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if password:
        assert response.status_code == status_map['update_upload_post'][username], response.content
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_upload_post_error(db, settings, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_update_upload', args=[project_id])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'error.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if password:
        assert response.status_code == status_map['update_upload_error'][username], response.content
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_upload_post_empty(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_update_upload', args=[project_id])
    response = client.post(url)
    if password:
        assert response.status_code == status_map['update_upload_empty'][username], response.content
        if response.status_code == 302:
            assert response.url == '/projects/{}/'.format(project_id), response.content
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_import_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_update_import', args=[project_id])
    response = client.get(url)
    if password:
        assert response.status_code == status_map['update_import_get'][username], response.content
        if response.status_code == 302:
            assert response.url == '/projects/{}/'.format(project_id), response.content
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_import_post(db, settings, client, username, password):
    client.login(username=username, password=password)

    # upload file
    url = reverse('project_update_upload', args=[project_id])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if password:
        assert response.status_code == status_map['update_upload_post'][username], response.content

        # get keys from the response
        keys = re.findall(r'name=\"(.*?)\"', response.content.decode())

        # import file
        url = reverse('project_update_import', args=[project_id])
        data = {key: ['on'] for key in keys}
        response = client.post(url, data)

        # no new project, snapshots, values were created
        project = Project.objects.get(pk=project_id)
        assert Project.objects.count() == 1
        assert project.snapshots.count() == 2
        assert project.values.count() == 225
        assert project.values.filter(snapshot=None).count() == 75
        assert timezone.now() - project.updated > timedelta(days=1)
        for snapshot in project.snapshots.all():
            assert timezone.now() - snapshot.updated > timedelta(days=1)
            for value in snapshot.values.all():
                assert timezone.now() - value.updated > timedelta(days=1)

        if password:
            assert response.status_code == status_map['update_import_post'][username], response.content
            if response.status_code == 302:
                assert response.url == '/projects/{}/'.format(project_id)

                for value in project.values.filter(snapshot=None):
                    assert timezone.now() - value.updated < timedelta(days=1)
            else:
                for value in project.values.filter(snapshot=None):
                    assert timezone.now() - value.updated > timedelta(days=1)
        else:
            assert response.status_code == 302, response.content
            assert response.url.startswith('/account/login/'), response.content
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_import_post_error(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_update_import', args=[project_id])
    response = client.post(url)
    if password:
        assert response.status_code == status_map['update_import_error'][username], response.content
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content


@pytest.mark.parametrize('username,password', users)
def test_project_update_import_empty(db, settings, client, username, password):
    client.login(username=username, password=password)

    # upload file
    url = reverse('project_update_upload', args=[project_id])
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    with open(xml_file, encoding='utf8') as f:
        response = client.post(url, {'uploaded_file': f})

    if password:
        assert response.status_code == status_map['update_upload_post'][username], response.content

        response = client.post(url)

        # no new project, snapshots, values were created
        project = Project.objects.get(pk=project_id)
        assert Project.objects.count() == 1
        assert project.snapshots.count() == 2
        assert project.values.count() == 225
        assert project.values.filter(snapshot=None).count() == 75
        assert timezone.now() - project.updated > timedelta(days=1)
        for value in project.values.filter(snapshot=None):
            assert timezone.now() - value.updated > timedelta(days=1)
        for snapshot in project.snapshots.all():
            assert timezone.now() - snapshot.updated > timedelta(days=1)
            for value in snapshot.values.all():
                assert timezone.now() - value.updated > timedelta(days=1)

        if password:
            assert response.status_code == status_map['update_import_post'][username], response.content
            if response.status_code == 302:
                assert response.url == '/projects/{}/'.format(project_id)
        else:
            assert response.status_code == 302, response.content
            assert response.url.startswith('/account/login/'), response.content
    else:
        assert response.status_code == 302, response.content
        assert response.url.startswith('/account/login/'), response.content
