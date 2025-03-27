import pytest

from django.urls import reverse

from ..models import Project, Visibility

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('api', 'api'),
    ('site', 'site'),
    ('anonymous', None)
)


project_id = 12

@pytest.mark.parametrize('username,password', users)
def test_project_create_visibility_get(db, client, username, password):
    client.login(username=username, password=password)

    project = Project.objects.get(id=project_id)
    project.visibility.delete()

    url = reverse('project_update_visibility', args=[project_id])
    response = client.get(url)

    if username in ['admin', 'site', 'api']:
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
def test_project_create_visibility_post(db, client, username, password):
    client.login(username=username, password=password)

    project = Project.objects.get(id=project_id)
    project.visibility.delete()

    url = reverse('project_update_visibility', args=[project_id])
    data = {}
    response = client.post(url, data)

    if username in ['admin', 'site', 'api']:
        assert response.status_code == 302
        assert Project.objects.get(pk=project_id).visibility
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302

        with pytest.raises(Visibility.DoesNotExist):
            assert Project.objects.get(pk=project_id).visibility


def test_project_create_visibility_get_create(db, client, settings):
    client.login(username='site', password='site')

    project = Project.objects.get(id=project_id)
    project.visibility.delete()

    url = reverse('project_update_visibility', args=[project_id])
    response = client.get(url)

    assert response.status_code == 200
    assert b'value="Make visible"' in response.content
    assert b'value="Remove visibility"' not in response.content


def test_project_create_visibility_get_remove(db, client, settings):
    client.login(username='site', password='site')

    url = reverse('project_update_visibility', args=[project_id])
    response = client.get(url)

    assert response.status_code == 200
    assert b'value="Make visible"' not in response.content
    assert b'value="Remove visibility"' in response.content


def test_project_create_visibility_get_create_site(db, client, settings):
    settings.MULTISITE = True

    client.login(username='site', password='site')

    project = Project.objects.get(id=project_id)
    project.visibility.delete()

    url = reverse('project_update_visibility', args=[project_id])
    response = client.get(url)

    assert response.status_code == 200
    assert b'value="Make visible"' in response.content
    assert b'value="Remove visibility"' not in response.content


def test_project_create_visibility_get_create_site_existing(db, client, settings):
    settings.MULTISITE = True

    client.login(username='site', password='site')

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set([2, 3])

    url = reverse('project_update_visibility', args=[project_id])
    response = client.get(url)

    assert response.status_code == 200
    assert b'value="Make visible for this site"' in response.content
    assert b'value="Remove visibility"' not in response.content


def test_project_create_visibility_get_remove_site(db, client, settings):
    settings.MULTISITE = True

    client.login(username='site', password='site')

    url = reverse('project_update_visibility', args=[project_id])
    response = client.get(url)

    assert response.status_code == 200
    assert b'value="Update visibility"' not in response.content
    assert b'value="Remove visibility"' in response.content


def test_project_create_visibility_get_update_site_group(db, client, settings):
    settings.MULTISITE = True
    settings.GROUPS = True

    client.login(username='site', password='site')

    url = reverse('project_update_visibility', args=[project_id])
    response = client.get(url)

    assert response.status_code == 200
    assert b'value="Update visibility"' in response.content
    assert b'value="Remove visibility"' in response.content


def test_project_create_visibility_get_create_group(db, client, settings):
    settings.GROUPS = True

    client.login(username='site', password='site')

    project = Project.objects.get(id=project_id)
    project.visibility.delete()

    url = reverse('project_update_visibility', args=[project_id])
    response = client.get(url)

    assert response.status_code == 200
    assert b'value="Make visible"' in response.content
    assert b'value="Remove visibility"' not in response.content


def test_project_create_visibility_get_remove_group(db, client, settings):
    settings.GROUPS = True

    client.login(username='site', password='site')

    url = reverse('project_update_visibility', args=[project_id])
    response = client.get(url)

    assert response.status_code == 200
    assert b'value="Update visibility"' in response.content
    assert b'value="Remove visibility"' in response.content


def test_project_update_visibility_site_post_add(db, client, settings):
    settings.MULTISITE = True

    client.login(username='site', password='site')

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set([])

    url = reverse('project_update_visibility', args=[project_id])
    data = {}
    response = client.post(url, data)

    assert response.status_code == 302

    project = Project.objects.get(id=project_id)

    assert project.visibility
    assert [site.id for site in project.visibility.sites.all()] == [1]
    assert not project.visibility.groups.exists()


def test_project_update_visibility_site_post_add_double(db, client, settings):
    settings.MULTISITE = True

    client.login(username='site', password='site')

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set([1])

    url = reverse('project_update_visibility', args=[project_id])
    data = {}
    response = client.post(url, data)

    assert response.status_code == 302

    project = Project.objects.get(id=project_id)

    assert project.visibility
    assert [site.id for site in project.visibility.sites.all()] == [1]
    assert not project.visibility.groups.exists()


def test_project_update_visibility_site_post_add_additional(db, client, settings):
    settings.MULTISITE = True

    client.login(username='site', password='site')

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set([2])

    url = reverse('project_update_visibility', args=[project_id])
    data = {}
    response = client.post(url, data)

    assert response.status_code == 302

    project = Project.objects.get(id=project_id)

    assert project.visibility
    assert [site.id for site in project.visibility.sites.all()] == [1, 2]
    assert not project.visibility.groups.exists()


def test_project_update_visibility_site_post_remove(db, client, settings):
    settings.MULTISITE = True

    client.login(username='site', password='site')

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set([1, 2, 3])

    url = reverse('project_update_visibility', args=[project_id])
    data = {
        'delete': 'true'
    }
    response = client.post(url, data)

    assert response.status_code == 302

    project = Project.objects.get(id=project_id)

    assert project.visibility
    assert {site.id for site in project.visibility.sites.all()} == {2, 3}
    assert not project.visibility.groups.exists()


def test_project_update_visibility_site_post_remove_last(db, client, settings):
    settings.MULTISITE = True

    client.login(username='site', password='site')

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set([1])

    url = reverse('project_update_visibility', args=[project_id])
    data = {
        'delete': 'true'
    }
    response = client.post(url, data)

    assert response.status_code == 302

    project = Project.objects.get(id=project_id)

    with pytest.raises(Visibility.DoesNotExist):
        project.visibility


def test_project_update_visibility_site_post_remove_empty(db, client, settings):
    settings.MULTISITE = True

    client.login(username='site', password='site')

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set([])

    url = reverse('project_update_visibility', args=[project_id])
    data = {
        'delete': 'true'
    }
    response = client.post(url, data)

    assert response.status_code == 302

    project = Project.objects.get(id=project_id)

    assert project.visibility
    assert {site.id for site in project.visibility.sites.all()} == {2, 3}
    assert not project.visibility.groups.exists()


def test_project_update_visibility_site_post_error(db, client, settings):
    settings.MULTISITE = True

    client.login(username='site', password='site')

    url = reverse('project_update_visibility', args=[project_id])
    data = {
        'sites': [2]
    }
    response = client.post(url, data)

    assert response.status_code == 302

    project = Project.objects.get(id=project_id)

    assert project.visibility
    assert [site.id for site in project.visibility.sites.all()] == [1]  # nothing changed
    assert not project.visibility.groups.exists()


def test_project_update_visibility_site_post_admin(db, client, settings):
    settings.MULTISITE = True

    client.login(username='admin', password='admin')

    url = reverse('project_update_visibility', args=[project_id])
    data = {
        'sites': [2]
    }
    response = client.post(url, data)

    assert response.status_code == 302

    project = Project.objects.get(id=project_id)

    assert project.visibility
    assert [site.id for site in project.visibility.sites.all()] == [2]
    assert not project.visibility.groups.exists()


def test_project_update_visibility_group_post(db, client, settings):
    settings.GROUPS = True

    client.login(username='site', password='site')

    url = reverse('project_update_visibility', args=[project_id])
    data = {
        'groups': [2]
    }
    response = client.post(url, data)

    assert response.status_code == 302

    project = Project.objects.get(id=project_id)

    assert project.visibility
    assert [site.id for site in project.visibility.sites.all()] == [1]  # this site is in the fixture
    assert [group.id for group in project.visibility.groups.all()] == [2]


def test_project_update_visibility_site_group_post_admin(db, client, settings):
    settings.MULTISITE = True
    settings.GROUPS = True

    client.login(username='admin', password='admin')

    url = reverse('project_update_visibility', args=[project_id])
    data = {
        'sites': [2],
        'groups': [2]
    }
    response = client.post(url, data)

    assert response.status_code == 302

    project = Project.objects.get(id=project_id)

    assert project.visibility
    assert [site.id for site in project.visibility.sites.all()] == [2]
    assert [group.id for group in project.visibility.groups.all()] == [2]


@pytest.mark.parametrize('username,password', users)
def test_project_delete_visibility_post(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('project_update_visibility', args=[project_id])
    data = {
        'delete': 'some value'
    }
    response = client.post(url, data)

    if username in ['admin', 'site', 'api']:
        assert response.status_code == 302
        with pytest.raises(Visibility.DoesNotExist):
            assert Project.objects.get(pk=project_id).visibility
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302

        assert Project.objects.get(pk=project_id).visibility
