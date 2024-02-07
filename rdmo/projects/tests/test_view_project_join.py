import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Invite, Membership, Project

membership_roles = ('owner', 'manager', 'author', 'guest')


@pytest.fixture()
def use_project_invite_timeout(settings):
    settings.PROJECT_INVITE_TIMEOUT = -1


@pytest.mark.parametrize('membership_role', membership_roles)
def test_project_join(db, client, membership_role):
    client.login(username='user', password='user')

    project = Project.objects.get(id=1)
    user = get_user_model().objects.get(username='user')
    invite = Invite(project=project, user=user, role=membership_role)
    invite.make_token()
    invite.save()

    url = reverse('project_join', args=[invite.token])
    response = client.get(url)

    assert response.status_code == 302
    assert Membership.objects.get(project=project, user=user, role=membership_role)


@pytest.mark.parametrize('membership_role', membership_roles)
def test_project_join_mail(db, client, membership_role):
    client.login(username='user', password='user')

    project = Project.objects.get(id=1)
    user = get_user_model().objects.get(username='user')
    invite = Invite(project=project, user=None, role=membership_role)
    invite.make_token()
    invite.save()

    url = reverse('project_join', args=[invite.token])
    response = client.get(url)

    assert response.status_code == 302
    assert Membership.objects.get(project=project, user=user, role=membership_role)


@pytest.mark.parametrize('membership_role', membership_roles)
def test_project_join_mail_existing_user(db, client, membership_role):
    client.login(username='author', password='author')

    project = Project.objects.get(id=1)
    user = get_user_model().objects.get(username='author')
    invite = Invite(project=project, user=None, role=membership_role)
    invite.make_token()
    invite.save()

    url = reverse('project_join', args=[invite.token])
    response = client.get(url)

    membership = Membership.objects.get(project=project, user=user)

    assert response.status_code == 302
    assert membership.role == 'author'


@pytest.mark.parametrize('membership_role', membership_roles)
def test_project_join_error(db, client, membership_role):
    client.login(username='user', password='user')

    project = Project.objects.get(id=1)
    user = get_user_model().objects.get(username='user')
    invite = Invite(project=project, user=user, role=membership_role)
    invite.make_token()
    invite.save()

    url = reverse('project_join', args=['wrong'])
    response = client.get(url)

    assert response.status_code == 200
    assert b'is not valid' in response.content
    assert not Membership.objects.filter(project=project, user=user, role=membership_role).exists()


@pytest.mark.parametrize('membership_role', membership_roles)
def test_project_join_timeout_error(db, client, membership_role, use_project_invite_timeout):
    client.login(username='user', password='user')

    project = Project.objects.get(id=1)
    user = get_user_model().objects.get(username='user')
    invite = Invite(project=project, user=user, role=membership_role)
    invite.make_token()
    invite.save()

    url = reverse('project_join', args=[invite.token])
    response = client.get(url)

    assert response.status_code == 200
    assert b'expired' in response.content
    assert not Membership.objects.filter(project=project, user=user, role=membership_role).exists()


@pytest.mark.parametrize('membership_role', membership_roles)
def test_project_join_user_error(db, client, membership_role):
    client.login(username='user', password='user')

    project = Project.objects.get(id=1)
    user = get_user_model().objects.get(username='user')
    invite = Invite(project=project, user=get_user_model().objects.get(username='guest'), role=membership_role)
    invite.make_token()
    invite.save()

    url = reverse('project_join', args=[invite.token])
    response = client.get(url)

    assert response.status_code == 200
    assert b'guest' in response.content
    assert not Membership.objects.filter(project=project, user=user, role=membership_role).exists()
