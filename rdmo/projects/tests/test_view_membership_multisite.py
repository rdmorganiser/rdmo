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

add_membership_permission_map = {
    'owner': [1, 2, 3, 4, 5],
    'api': [1, 2, 3, 4, 5],
    'site': [1, 2, 3, 4, 5]
}

projects = [1, 2, 3, 4, 5]
memberships = [1, 2, 3, 4]

membership_roles = ('owner', 'manager', 'author', 'guest')

sites_domains = ('example.com', 'foo.com', 'bar.com')


@pytest.fixture()
def multisite(settings):
    settings.MULTISITE = True


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('membership_role', membership_roles)
@pytest.mark.parametrize('site_domain', sites_domains)
def test_get_invite_email_project_path_function(db, client, username, password, project_id,
                                                membership_role, site_domain, multisite):
    client.login(username=username, password=password)

    current_site = Site.objects.get_current()
    foo_site, _created = Site.objects.get_or_create(domain=site_domain, name=site_domain)
    foo_username = f'{site_domain}-test-user'
    foo_email = f'{foo_username}@{site_domain}'
    foo_user, _created = get_user_model().objects.get_or_create(username=foo_username, email=foo_email,
                                                                password=foo_username)
    foo_user.role.member.set([foo_site])
    project = Project.objects.get(pk=project_id)

    invite = Invite(project=project, user=foo_user, role=membership_role)
    invite.make_token()
    invite.save()

    invite_email_project_path = get_invite_email_project_path(invite)
    if current_site.domain == site_domain:
        assert invite_email_project_path.startswith('/projects')
    else:
        assert invite_email_project_path.startswith('http://' + site_domain + '/projects')


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('project_id', projects)
@pytest.mark.parametrize('membership_role', membership_roles)
@pytest.mark.parametrize('site_domain', sites_domains)
def test_invite_email_project_path_email_body(db, client, username, password, project_id,
                                              membership_role, site_domain, multisite):
    client.login(username=username, password=password)

    current_site = Site.objects.get_current()
    foo_site, _created = Site.objects.get_or_create(domain=site_domain, name=site_domain)
    foo_username = f'{site_domain}-user'
    foo_email = f'{foo_username}@{site_domain}'
    foo_user, _created = get_user_model().objects.get_or_create(username=f'{site_domain}-user', email=foo_email,
                                                                password=foo_username)
    foo_user.role.member.set([foo_site])
    project = Project.objects.get(pk=project_id)

    url = reverse('membership_create', args=[project_id])
    data = {
        'username_or_email': foo_email,
        'role': membership_role
    }
    response = client.post(url, data)

    invite = Invite(project=project, user=foo_user, role=membership_role)
    invite.make_token()
    invite.save()

    if project_id in add_membership_permission_map.get(username, []):
        if current_site.domain == site_domain:
            assert 'http://testserver/' in mail.outbox[0].body
        else:
            assert f'http://{foo_site.domain}/' in mail.outbox[0].body

        assert response.status_code == 302
        assert len(mail.outbox) == 1
    else:
        if password:
            assert response.status_code == 403
        else:
            assert response.status_code == 302
        assert len(mail.outbox) == 0
