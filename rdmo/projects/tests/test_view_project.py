import re

import pytest

from django.urls import reverse

from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from rdmo.questions.models import Catalog
from rdmo.views.models import View

from ..forms import CatalogChoiceField
from ..models import Project

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('api', 'api'),
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
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
}

delete_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
}

export_project_permission_map = {
    'owner': [1, 2, 3, 4, 5, 10],
    'manager': [1, 3, 5, 7],
    'api': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'site': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
}

projects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

export_formats = ('rtf', 'odt', 'docx', 'html', 'markdown', 'tex', 'pdf')

site_id = 1
parent_project_id = 1
catalog_id = 1


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('projects')
    response = client.get(url)

    projects = re.findall(r'/projects/(\d+)/', response.content.decode())

    if password:
        assert response.status_code == 200
        assertTemplateUsed(response, 'projects/projects.html')

        if username in ('site', 'api'):
            assert projects == []
            assert response.context['number_of_projects'] == len([])
            assertContains(response, 'View all projects on')
        else:
            user_projects_map = view_project_permission_map.get(username, [])
            assert sorted(set(map(int, projects))) == user_projects_map
            assert response.context['number_of_projects'] == len(user_projects_map)
            assertNotContains(response, 'View all projects on')
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
def test_site(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('site_projects')
    response = client.get(url)

    projects = re.findall(r'/projects/(\d+)/update/', response.content.decode())

    if password:
        if username in ('site', 'api'):
            assert response.status_code == 200
            assertTemplateUsed(response, 'projects/site_projects.html')
            user_projects_map = view_project_permission_map.get(username, [])
            assert sorted(set(map(int, projects))) == user_projects_map
            assert response.context['number_of_projects'] == len(user_projects_map)
        else:
            assert response.status_code == 403
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_detail(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project', args=[project_id])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
def test_project_create_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_create')
    response = client.get(url)

    if password:
        assert response.status_code == 200

        # check the parent select dropdown
        for project_id in re.findall(r'<option value="(\d+)"', response.content.decode()):
            assert int(project_id) in view_project_permission_map.get(username, [])
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
def test_project_create_get_for_extra_users_and_unavailable_catalogs(db, client, username, password):
    client.login(username=username, password=password)

    Catalog.objects.create(
        uri_prefix='https://experimental.com/terms',
        uri_path='unavailable-1',
        order=1,
        title_lang1='New Catalog 1',
        title_lang2='Neuer Katalog 1',
        help_lang1='Help text',
        help_lang2='Hilfe Text',
        available=False
    )

    Catalog.objects.create(
        uri_prefix='https://experimental.com/terms',
        uri_path='unavailable-2',
        order=2,
        title_lang1='New Catalog 2',
        title_lang2='Neuer Katalog 2',
        help_lang1='Help text',
        help_lang2='Hilfe Text',
        available=False
    )

    url = reverse('project_create')
    response = client.get(url)

    if password:
        assert response.status_code == 200
        # check the catalogs that are displayed in the form
        find_catalog_ids = re.findall(r'id="id_catalog_(\d+)', response.content.decode())
        catalogs_in_form = response.context_data['form'].fields['catalog'].queryset
        assert find_catalog_ids == list(map(str, range(catalogs_in_form.count())))

        # check the unavailable catalogs that are displayed in the form
        # should happen only for users that can see unavailable catalogs (editors, api,..)
        for unavailable_catalog in catalogs_in_form.filter(available=False):
            _label = unavailable_catalog.title + CatalogChoiceField._unavailable_icon
            assert _label in response.content.decode()

        # check the parent select dropdown
        for project_id in re.findall(r'<option value="(\d+)"', response.content.decode()):
            assert int(project_id) in view_project_permission_map.get(username, [])
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
def test_project_create_post(db, client, username, password):
    client.login(username=username, password=password)
    project_count = Project.objects.count()

    url = reverse('project_create')
    data = {
        'title': 'A new project',
        'description': 'Some description',
        'catalog': catalog_id
    }
    response = client.post(url, data)

    if password:
        assert response.status_code == 302
        assert Project.objects.count() == project_count + 1
    else:
        assert response.status_code == 302
        assert Project.objects.count() == project_count


@pytest.mark.parametrize('username,password', users)
def test_project_create_parent_post(db, client, username, password):
    client.login(username=username, password=password)
    project_count = Project.objects.count()

    url = reverse('project_create')
    data = {
        'title': 'A new project',
        'description': 'Some description',
        'catalog': catalog_id,
        'parent': parent_project_id
    }
    response = client.post(url, data)

    if username in ('user', 'editor', 'reviewer'):
        assert response.status_code == 200
        assert Project.objects.count() == project_count
    elif password:
        assert response.status_code == 302
        assert Project.objects.count() == project_count + 1
    else:
        assert response.status_code == 302
        assert Project.objects.count() == project_count


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update', args=[project_id])
    response = client.get(url)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_post(db, client, username, password, project_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)

    url = reverse('project_update', args=[project_id])
    data = {
        'title': 'New title',
        'description': project.description,
        'catalog': project.catalog.pk
    }
    response = client.post(url, data)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 302
        assert Project.objects.get(pk=project_id).title == 'New title'
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302

        assert Project.objects.get(pk=project_id).title == project.title


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_post_parent(db, client, username, password, project_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)

    url = reverse('project_update', args=[project_id])
    data = {
        'title': project.title,
        'description': project.description,
        'catalog': project.catalog.pk,
        'parent': parent_project_id
    }
    response = client.post(url, data)

    if project_id in change_project_permission_map.get(username, []):
        if project_id == parent_project_id:
            assert response.status_code == 200
            assert Project.objects.get(pk=project_id).parent == project.parent
        else:
            assert response.status_code == 302
            assert Project.objects.get(pk=project_id).parent_id == parent_project_id
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302

        assert Project.objects.get(pk=project_id).parent == project.parent


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_information_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_information', args=[project_id])
    response = client.get(url)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_information_post(db, client, username, password, project_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)

    url = reverse('project_update_information', args=[project_id])
    data = {
        'title': 'Lorem ipsum dolor sit amet',
        'description': 'At vero eos et accusam et justo duo dolores et ea rebum.'
    }
    response = client.post(url, data)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 302
        assert Project.objects.get(pk=project_id).title == 'Lorem ipsum dolor sit amet'
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302

        assert Project.objects.get(pk=project_id).title == project.title


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_catalog_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_catalog', args=[project_id])
    response = client.get(url)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_catalog_post(db, client, username, password, project_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)

    url = reverse('project_update_catalog', args=[project_id])
    data = {
        'catalog': catalog_id
    }
    response = client.post(url, data)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 302
        assert Project.objects.get(pk=project_id).catalog_id == catalog_id
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302

        assert Project.objects.get(pk=project_id).catalog == project.catalog


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_tasks_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_tasks', args=[project_id])
    response = client.get(url)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_tasks_post(db, client, username, password, project_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)

    url = reverse('project_update_tasks', args=[project_id])
    data = {
        'tasks': []
    }
    response = client.post(url, data)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 302
        assert list(Project.objects.get(pk=project_id).tasks.values('id')) == []
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302

        assert list(Project.objects.get(pk=project_id).tasks.values('id')) == list(project.tasks.values('id'))


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_views_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_views', args=[project_id])
    response = client.get(url)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_views_post(db, client, username, password, project_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)

    url = reverse('project_update_views', args=[project_id])
    data = {
        'views': []
    }
    response = client.post(url, data)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 302
        assert list(Project.objects.get(pk=project_id).views.values('id')) == []
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302

        assert list(Project.objects.get(pk=project_id).views.values('id')) == list(project.views.values('id'))


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_parent_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_update_parent', args=[project_id])
    response = client.get(url)

    if project_id in change_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_update_parent_post(db, client, username, password, project_id):
    client.login(username=username, password=password)
    project = Project.objects.get(pk=project_id)

    url = reverse('project_update_parent', args=[project_id])
    data = {
        'parent': parent_project_id
    }
    response = client.post(url, data)

    if project_id in change_project_permission_map.get(username, []):
        if project_id == parent_project_id:
            assert response.status_code == 200
            assert Project.objects.get(pk=project_id).parent == project.parent
        else:
            assert response.status_code == 302
            assert Project.objects.get(pk=project_id).parent_id == parent_project_id
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302

        assert Project.objects.get(pk=project_id).parent == project.parent


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_delete_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_delete', args=[project_id])
    response = client.get(url)

    if project_id in delete_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_delete_post(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_delete', args=[project_id])
    response = client.post(url)

    if project_id in delete_project_permission_map.get(username, []):
        assert response.status_code == 302
        assert not Project.objects.filter(pk=project_id).first()
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302

        assert Project.objects.filter(pk=project_id).first()


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_export_xml(db, client, files, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_export', args=[project_id, 'xml'])
    response = client.get(url)

    if project_id in export_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_export_csv(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_export', args=[project_id, 'csvcomma'])
    response = client.get(url)

    if project_id in export_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_export_csvsemicolon(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_export', args=[project_id, 'csvsemicolon'])
    response = client.get(url)

    if project_id in export_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_export_json(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_export', args=[project_id, 'json'])
    response = client.get(url)

    if project_id in export_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_answers(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_answers', args=[project_id])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('export_format', export_formats)
def test_project_answers_export(db, client, username, password, project_id, export_format):
    client.login(username=username, password=password)

    url = reverse('project_answers_export', args=[project_id, export_format])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_view(db, client, username, password, project_id):
    client.login(username=username, password=password)
    project_views = Project.objects.get(pk=project_id).views.all()

    for view in View.objects.all():
        url = reverse('project_view', args=[project_id, view.id])
        response = client.get(url)

        if project_id in view_project_permission_map.get(username, []):
            if view in project_views:
                assert response.status_code == 200
            else:
                assert response.status_code == 404
        else:
            if password:
                assert response.status_code == 403
            else:
                assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('export_format', export_formats)
def test_project_view_export(db, client, username, password, project_id, export_format, files):
    client.login(username=username, password=password)
    project_views = Project.objects.get(pk=project_id).views.all()

    for view in View.objects.all():
        url = reverse('project_view_export', args=[project_id, view.pk, export_format])
        response = client.get(url)

        if project_id in view_project_permission_map.get(username, []):
            if view in project_views:
                assert response.status_code == 200
            else:
                assert response.status_code == 404
        else:
            if password:
                assert response.status_code == 403
            else:
                assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_questions(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_questions', args=[project_id])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_error(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_questions', args=[project_id])
    response = client.get(url)

    if project_id in view_project_permission_map.get(username, []):
        assert response.status_code == 200
    elif password:
        assert response.status_code == 403
    else:
        assert response.status_code == 302
