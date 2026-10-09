import pytest

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core import mail
from django.urls import reverse

from ..models import Invite, Project
from ..utils import get_invite_email_project_path

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

urlnames = {
    'list': 'v1-projects:project-invite-list',
}

view_invite_permission_map = {
    'owner': [1],
    'manager': [],
    'author': [],
    'guest': [],
    'api': [1, 11],
    'site': [1, 11]
}

add_invite_permission_map = {
    'owner': [1],
    'api': [1, 11],
    'site': [1, 11]
}

projects = [1, 11]
invites = [1, 2]

membership_roles = (
    'owner',
    'manager',
    'author',
    'guest'
)

sites_domains = (
    'example.com',
    'foo.com',
    'bar.com'
)


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('membership_role', membership_roles)
@pytest.mark.parametrize('site_domain', sites_domains)
def test_get_invite_email_project_path_function(
    rf, db, client, settings, username, password, project_id, membership_role, site_domain
):
    settings.MULTISITE = True

    client.login(username=username, password=password)

    current_site = Site.objects.get_current()
    site = Site.objects.get(domain=site_domain)

    user_username = f'{site_domain}-test-user'
    user_email = f'{user_username}@{site_domain}'
    user = get_user_model().objects.create(username=user_username, email=user_email, password=user_username)
    user.role.member.set([site])

    project = Project.objects.get(pk=project_id)

    invite = Invite(project=project, user=user, role=membership_role)
    invite.make_token()
    invite.save()

    request = rf.get('/')
    invite_email_project_path = get_invite_email_project_path(request, invite)
    if current_site.domain == site_domain:
        assert invite_email_project_path.startswith('http://testserver/projects')
    else:
        assert invite_email_project_path.startswith(f'http://{site_domain}/projects')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('membership_role', membership_roles)
@pytest.mark.parametrize('site_domain', sites_domains)
def test_invite_email_project_path_email_body(
    db, client, settings, username, password, project_id, membership_role, site_domain
):
    settings.MULTISITE = True

    Invite.objects.all().delete()

    client.login(username=username, password=password)

    current_site = Site.objects.get_current()
    site = Site.objects.get(domain=site_domain)

    user_username = f'{site_domain}-test-user'
    user_email = f'{user_username}@{site_domain}'
    user = get_user_model().objects.create(username=user_username, email=user_email, password=user_username)
    user.role.member.set([site])

    project = Project.objects.get(pk=project_id)

    url = reverse(urlnames['list'], args=[project_id])
    data = {
        'user': user.id,
        'role': membership_role
    }
    response = client.post(url, data)


    if project_id in add_invite_permission_map.get(username, []):
        assert response.status_code == 201
        assert Invite.objects.get(project_id=project.id, user=user, role=membership_role)

        assert len(mail.outbox) == 1

        if current_site.domain == site_domain:
            assert 'http://testserver/' in mail.outbox[0].body
        else:
            assert f'http://{site_domain}/projects' in mail.outbox[0].body

    else:
        if project_id in view_invite_permission_map.get(username, []):
            assert response.status_code == 403
        else:
            assert response.status_code == 404

        assert not Invite.objects.exists()
        assert len(mail.outbox) == 0
