from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from django.urls import reverse

from ..models import Project

user_username = 'user'
project_id = 12


def test_detail_cleared(db, client):
    client.login(username='user', password='user')

    project = Project.objects.get(id=project_id)
    project.visibility.sites.clear()
    project.visibility.groups.clear()

    url = reverse('project', args=[project_id])
    response = client.get(url)
    assert response.status_code == 200


def test_detail_deleted(db, client):
    client.login(username='user', password='user')

    project = Project.objects.get(id=project_id)
    project.visibility.delete()

    url = reverse('project', args=[project_id])
    response = client.get(url)
    assert response.status_code == 403


def test_detail_site(db, client):
    client.login(username='user', password='user')

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set(Site.objects.filter(id=1))
    project.visibility.groups.clear()

    url = reverse('project', args=[project_id])
    response = client.get(url)
    assert response.status_code == 200


def test_detail_multiple_sites(db, client):
    client.login(username='user', password='user')

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set(Site.objects.filter(id__in=[1, 2]))
    project.visibility.groups.clear()

    url = reverse('project', args=[project_id])
    response = client.get(url)
    assert response.status_code == 200


def test_detail_site_forbidden(db, client):
    client.login(username='user', password='user')

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set(Site.objects.filter(id=2))
    project.visibility.groups.clear()

    url = reverse('project', args=[project_id])
    response = client.get(url)
    assert response.status_code == 403


def test_detail_group(db, client):
    client.login(username='user', password='user')

    group = Group.objects.create(name='test')
    user = User.objects.get(username='user')
    user.groups.add(group)

    project = Project.objects.get(id=project_id)
    project.visibility.sites.clear()
    project.visibility.groups.add(group)

    url = reverse('project', args=[project_id])
    response = client.get(url)
    assert response.status_code == 200


def test_detail_multiple_groups(db, client):
    client.login(username='user', password='user')

    group = Group.objects.create(name='test')
    user = User.objects.get(username='user')
    user.groups.add(group)

    project = Project.objects.get(id=project_id)
    project.visibility.sites.clear()
    project.visibility.groups.set([
        group, Group.objects.create(name='test2')
    ])

    url = reverse('project', args=[project_id])
    response = client.get(url)
    assert response.status_code == 200


def test_detail_group_forbidden(db, client):
    client.login(username='user', password='user')

    group = Group.objects.create(name='test')

    project = Project.objects.get(id=project_id)
    project.visibility.sites.clear()
    project.visibility.groups.set([group])

    url = reverse('project', args=[project_id])
    response = client.get(url)
    assert response.status_code == 403


def test_detail_site_group(db, client):
    client.login(username='user', password='user')

    group = Group.objects.create(name='test')
    user = User.objects.get(username='user')
    user.groups.add(group)

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set(Site.objects.filter(id=1))
    project.visibility.groups.set([group])

    url = reverse('project', args=[project_id])
    response = client.get(url)
    assert response.status_code == 200


def test_detail_site_group_forbidden(db, client):
    client.login(username='user', password='user')

    group = Group.objects.create(name='test')
    user = User.objects.get(username='user')
    user.groups.add(group)

    project = Project.objects.get(id=project_id)
    project.visibility.sites.set(Site.objects.filter(id=2))
    project.visibility.groups.set([group])

    url = reverse('project', args=[project_id])
    response = client.get(url)
    assert response.status_code == 403


# @pytest.mark.parametrize('username,password', users)
# @pytest.mark.parametrize('project_id', projects)
# def test_project_update_visibility_get(db, client, username, password, project_id):
#     client.login(username=username, password=password)

#     url = reverse('project_update_visibility', args=[project_id])
#     response = client.get(url)

#     if project_id in change_project_permission_map.get(username, []):
#         assert response.status_code == 200
#     else:
#         if password:
#             assert response.status_code == 403
#         else:
#             assert response.status_code == 302


# @pytest.mark.parametrize('username,password', users)
# @pytest.mark.parametrize('project_id', projects)
# def test_project_update_visibility_post(db, client, username, password, project_id):
#     client.login(username=username, password=password)
#     project = Project.objects.get(pk=project_id)

#     url = reverse('project_update_visibility', args=[project_id])
#     data = {
#         'visibility': 'internal'
#     }
#     response = client.post(url, data)

#     if project_id in change_project_permission_map.get(username, []):
#         assert response.status_code == 302
#         assert Project.objects.get(pk=project_id).visibility == 'internal'
#     else:
#         if password:
#             assert response.status_code == 403
#         else:
#             assert response.status_code == 302

#         assert Project.objects.get(pk=project_id).visibility == project.visibility
