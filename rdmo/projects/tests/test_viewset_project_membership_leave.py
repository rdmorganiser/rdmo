import pytest

from django.contrib.auth.models import User
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
    'owner': [1, 2, 3, 4, 5, 12],
    'manager': [1, 3],
    'author': [1, 3],
    'guest': [1, 3]
}

urlnames = {
    'leave': 'v1-projects:project-membership-leave',
}

projects = [1, 2, 3, 4, 5, 12]
memberships = [1, 2, 3, 4]
memberships_visible = [16]


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
def test_leave(db, client, username, password, project_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['leave'], args=[project_id])
    response = client.delete(url)

    # store if the membership exists
    membership_existed = Membership.objects.filter(project_id=project_id, user__username=username).exists()

    if project_id in leave_project_permission_map.get(username, []):
        if username == 'owner':
            assert response.status_code == 404  # last owner is not allowed to leave
        else:
            assert response.status_code == 204

            if membership_existed:
                assert not Membership.objects.filter(project_id=project_id, user__username=username).exists()
    else:
        assert response.status_code == 404


@pytest.mark.parametrize('project_id', projects)
def test_project_leave_post_last_owner(db, client, project_id):
    client.login(username='owner', password='owner')

    # store if the membership exists
    membership_existed = Membership.objects.filter(project_id=project_id, user__username='owner').exists()

    # add user as the second owner
    Membership.objects.create(project_id=project_id, user=User.objects.get(username='user'), role='owner')

    url = reverse(urlnames['leave'], args=[project_id])
    response = client.delete(url)

    if project_id in leave_project_permission_map.get('owner', []):
        assert response.status_code == 204

        if membership_existed:
            assert not Membership.objects.filter(project_id=project_id, user__username='owner').exists()
    else:
        assert response.status_code == 404
