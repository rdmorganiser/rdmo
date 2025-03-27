import pytest

from django.urls import reverse

from ..models import Project, Visibility

users = (
    ('admin', 'admin'),
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('api', 'api'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

project_id = 12

@pytest.mark.parametrize('username,password', users)
def test_project_visibility_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('v1-projects:project-visibility', args=[project_id])
    response = client.get(url)

    if username in ['admin', 'site', 'api']:
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
def test_project_visibility_get_not_found(db, client, username, password):
    client.login(username=username, password=password)

    project = Project.objects.get(id=project_id)
    project.visibility.delete()

    url = reverse('v1-projects:project-visibility', args=[project_id])
    response = client.get(url)

    if password:
        assert response.status_code == 404
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
def test_project_visibility_post_create(db, client, username, password):
    client.login(username=username, password=password)

    project = Project.objects.get(id=project_id)
    project.visibility.delete()

    url = reverse('v1-projects:project-visibility', args=[project_id])
    data = {}
    response = client.post(url, data)

    if username in ['admin', 'site', 'api']:
        assert response.status_code == 200
        assert Project.objects.get(pk=project_id).visibility
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401

        with pytest.raises(Visibility.DoesNotExist):
            assert Project.objects.get(pk=project_id).visibility


@pytest.mark.parametrize('username,password', users)
def test_project_visibility_post_update(db, client, username, password):
    client.login(username=username, password=password)

    project = Project.objects.get(id=project_id)
    project.visibility.sites.clear()
    project.visibility.groups.clear()

    url = reverse('v1-projects:project-visibility', args=[project_id])
    data = {
        'sites': [3],
        'groups': [3],
    }
    response = client.post(url, data)

    project = Project.objects.get(pk=project_id)

    if username in ['admin', 'site', 'api']:
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401

    assert project.visibility
    assert not project.visibility.sites.exists()
    assert not project.visibility.groups.exists()


@pytest.mark.parametrize('username,password', users)
def test_project_visibility_post_update_group(db, client, settings, username, password):
    settings.GROUPS = True

    client.login(username=username, password=password)

    project = Project.objects.get(id=project_id)
    project.visibility.groups.set([3])

    url = reverse('v1-projects:project-visibility', args=[project_id])
    data = {
        'groups': [2],
    }
    response = client.post(url, data)

    project = Project.objects.get(pk=project_id)

    if username in ['admin', 'site', 'api']:
        assert response.status_code == 200
        assert project.visibility
        assert [group.id for group in project.visibility.groups.all()] == [2]
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401

        assert project.visibility
        assert [group.id for group in project.visibility.groups.all()] == [3]


@pytest.mark.parametrize('username,password', users)
def test_project_visibility_post_update_site(db, client, settings, username, password):
    settings.MULTISITE = True

    client.login(username=username, password=password)

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set([3])

    url = reverse('v1-projects:project-visibility', args=[project_id])
    data = {
        'sites': [2],
    }
    response = client.post(url, data)

    project = Project.objects.get(pk=project_id)

    if username in ['admin']:
        assert response.status_code == 200
        assert project.visibility
        assert [site.id for site in project.visibility.sites.all()] == [2]
    elif username in ['site', 'api']:
        assert response.status_code == 200
        assert project.visibility
        assert {site.id for site in project.visibility.sites.all()} == {1, 3}
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401

        assert project.visibility
        assert [site.id for site in project.visibility.sites.all()] == [3]


@pytest.mark.parametrize('username,password', users)
def test_project_visibility_post_delete(db, client, username, password):
    client.login(username=username, password=password)

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set([1, 2, 3])

    url = reverse('v1-projects:project-visibility', args=[project_id])
    response = client.delete(url)

    project.refresh_from_db()

    if username in ['admin', 'site', 'api']:
        assert response.status_code == 204
        with pytest.raises(Visibility.DoesNotExist):
            assert project.visibility
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401

        assert project.visibility


@pytest.mark.parametrize('username,password', users)
def test_project_visibility_post_delete_site(db, client, settings, username, password):
    settings.MULTISITE = True

    client.login(username=username, password=password)

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set([1, 2, 3])

    url = reverse('v1-projects:project-visibility', args=[project_id])
    response = client.delete(url)

    project.refresh_from_db()

    if username in ['admin']:
        assert response.status_code == 204
        with pytest.raises(Visibility.DoesNotExist):
            assert project.visibility
    elif username in ['site', 'api']:
        assert response.status_code == 204
        assert project.visibility
        assert {site.id for site in project.visibility.sites.all()} == {2, 3}
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401

        assert project.visibility


@pytest.mark.parametrize('username,password', users)
def test_project_visibility_post_delete_site_last(db, client, settings, username, password):
    settings.MULTISITE = True

    client.login(username=username, password=password)

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set([1])

    url = reverse('v1-projects:project-visibility', args=[project_id])
    response = client.delete(url)

    project.refresh_from_db()

    if username in ['admin','site', 'api']:
        assert response.status_code == 204
        with pytest.raises(Visibility.DoesNotExist):
            assert project.visibility
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401
        assert project.visibility


@pytest.mark.parametrize('username,password', users)
def test_project_visibility_post_delete_site_empty(db, client, settings, username, password):
    settings.MULTISITE = True

    client.login(username=username, password=password)

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set([])

    url = reverse('v1-projects:project-visibility', args=[project_id])
    response = client.delete(url)

    project.refresh_from_db()

    if username in ['admin']:
        assert response.status_code == 204
        with pytest.raises(Visibility.DoesNotExist):
            assert project.visibility
    elif username in ['site', 'api']:
        assert response.status_code == 204
        assert project.visibility
        assert {site.id for site in project.visibility.sites.all()} == {2, 3}
    else:
        if password:
            assert response.status_code == 404
        else:
            assert response.status_code == 401
        assert project.visibility


@pytest.mark.parametrize('username,password', users)
def test_project_visibility_post_delete_not_found(db, client, username, password):
    client.login(username=username, password=password)

    project = Project.objects.get(pk=project_id)
    project.visibility.delete()

    url = reverse('v1-projects:project-visibility', args=[project_id])
    response = client.delete(url)

    if password:
        assert response.status_code == 404
    else:
        assert response.status_code == 401
