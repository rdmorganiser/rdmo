import pytest
from django.urls import reverse

from ..models import Membership

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

leave_project_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'manager': [1, 3],
    'author': [1, 3],
    'guest': [1, 3]
}

projects = [1, 2, 3, 4, 5]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_leave_get(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse('project_leave', args=[project_id])
    response = client.get(url)

    if project_id in leave_project_permission_map.get(username, []):
        assert response.status_code == 200
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_leave_post(db, client, username, password, project_id):
    client.login(username=username, password=password)

    # add additional owner, so that the owner can leave
    Membership.objects.create(user_id=1, project_id=project_id, role='owner')

    # store if the membership exists
    membership_existed = Membership.objects.filter(project_id=project_id, user__username=username).exists()

    url = reverse('project_leave', args=[project_id])
    response = client.post(url)

    if project_id in leave_project_permission_map.get(username, []):
        assert response.status_code == 302
        if membership_existed:
            assert not Membership.objects.filter(project_id=project_id, user__username=username).exists()
    else:
        if membership_existed:
            assert Membership.objects.filter(project_id=project_id, user__username=username).exists()

        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_leave_post_last_owner(db, client, username, password, project_id):
    client.login(username=username, password=password)

    # store if the membership exists
    membership_existed = Membership.objects.filter(project_id=project_id, user__username=username).exists()

    url = reverse('project_leave', args=[project_id])
    response = client.post(url)

    if project_id in leave_project_permission_map.get(username, []):
        assert response.status_code == 302

        if username == 'owner':
            if membership_existed:
                assert Membership.objects.filter(project_id=project_id, user__username=username).exists()
        else:
            if membership_existed:
                assert not Membership.objects.filter(project_id=project_id, user__username=username).exists()
    else:
        if membership_existed:
            assert Membership.objects.filter(project_id=project_id, user__username=username).exists()

        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_project_leave_post_cancel(db, client, username, password, project_id):
    client.login(username=username, password=password)

    # add additional owner, so that the owner can leave
    Membership.objects.create(user_id=1, project_id=project_id, role='owner')

    # store if the membership exists
    membership_existed = Membership.objects.filter(project_id=project_id, user__username=username).exists()

    url = reverse('project_leave', args=[project_id])
    response = client.post(url, {'cancel': True})

    if membership_existed:
        assert Membership.objects.filter(project_id=project_id, user__username=username).exists()

    if project_id in leave_project_permission_map.get(username, []):
        assert response.status_code == 302
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302


# @pytest.mark.parametrize('username,password', users)
# @pytest.mark.parametrize('project_id', projects)
# def test_project_leave_post(db, client, username, password, project_id):
#     client.login(username=username, password=password)

#     # add additional owner, so that the owner can leave
#     Membership.objects.create(user_id=1, project_id=project_id, role='owner')

#     url = reverse('project_leave', args=[project_id])
#     response = client.post(url)

#     if project_id in leave_project_permission_map.get(username, []):
#         assert response.status_code == 302
#         assert not Membership.objects.filter(project_id=project_id, user__username=username).exists()
#     else:
#         if password:
#             assert response.status_code == 403
#         else:
#             assert response.status_code == 302
