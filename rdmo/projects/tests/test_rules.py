import pytest

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from ..models import Project

users = (
    'owner',
    'manager',
    'author',
    'guest',
    'admin',
    'api',
    'site',
    'example-manager',
    'foo-manager',
    'bar-manager',
    'user',
)

permissions = (
    # project
    'projects.add_project',
    'projects.view_project_object',
    'projects.change_project_object',
    'projects.change_project_progress_object',
    'projects.delete_project_object',
    'projects.leave_project_object',
    'projects.export_project_object',
    'projects.import_project_object',
    # visibility
    'projects.view_visibility_object',
    'projects.add_visibility_object',
    'projects.change_visibility_object',
    'projects.delete_visibility_object',
    # membership
    'projects.view_membership_object',
    'projects.add_membership_object',
    'projects.change_membership_object',
    'projects.delete_membership_object',
    # invite
    'projects.view_invite_object',
    'projects.add_invite_object',
    'projects.change_invite_object',
    'projects.delete_invite_object',
    # integration
    'projects.view_integration_object',
    'projects.add_integration_object',
    'projects.change_integration_object',
    'projects.delete_integration_object',
    # issue
    'projects.view_issue_object',
    'projects.add_issue_object',
    'projects.change_issue_object',
    'projects.delete_issue_object',
    # snapshot
    'projects.view_snapshot_object',
    'projects.add_snapshot_object',
    'projects.change_snapshot_object',
    'projects.delete_snapshot_object',
    'projects.rollback_snapshot_object',
    'projects.export_snapshot_object',
    # value
    'projects.view_value_object',
    'projects.add_value_object',
    'projects.change_value_object',
    'projects.delete_value_object',
    # page
    'projects.view_page_object',
)

@pytest.mark.parametrize('permission', permissions)
@pytest.mark.parametrize('username', users)
def test_project(db, permission, username):
    user = User.objects.get(username=username)
    project = Project.objects.get(id=1)
    result = user.has_perm(permission, project)

    if permission == 'projects.add_project':
        # all users can create projects
        allowed = users

    elif permission in (
        'projects.add_visibility_object',
        'projects.add_membership_object',
        'projects.change_visibility_object',
        'projects.delete_visibility_object'
    ):
        # all users who act as site managers
        allowed = ('admin', 'api', 'site', 'example-manager')

    elif permission in (
        'projects.delete_project_object',
        'projects.change_membership_object',
        'projects.delete_membership_object',
        'projects.view_invite_object',
        'projects.add_invite_object',
        'projects.change_invite_object',
        'projects.delete_invite_object',
    ):
        # all users who act as owners of the project
        allowed = ('owner', 'admin', 'api', 'site', 'example-manager')

    elif permission in (
        'projects.change_project_object',
        'projects.import_project_object',
        'projects.export_project_object',
        'projects.add_integration_object',
        'projects.change_integration_object',
        'projects.delete_integration_object',
        'projects.add_issue_object',
        'projects.delete_issue_object',
        'projects.add_snapshot_object',
        'projects.change_snapshot_object',
        'projects.delete_snapshot_object',
        'projects.rollback_snapshot_object',
        'projects.export_snapshot_object',
    ):
        # all users who act as managers of the project
        allowed = ('owner', 'manager', 'admin', 'api', 'site', 'example-manager')

    elif permission in (
        'projects.change_project_progress_object',
        'projects.add_value_object',
        'projects.change_value_object',
        'projects.delete_value_object',
        'projects.change_issue_object'
    ):
        # all users who act as authors of the project
        allowed = ('owner', 'manager', 'author', 'admin', 'api', 'site', 'example-manager')

    elif permission.startswith('projects.view'):
        # all users who can access the project
        allowed = ('owner', 'manager', 'author', 'guest', 'admin', 'api', 'site', 'example-manager')

    elif permission == 'projects.leave_project_object':
        # any project member, but the last owner
        allowed = ('manager', 'author', 'guest', 'admin')  # TODO: check if admin can be removed

    else:
        allowed = []

    assert result == (username in allowed)


@pytest.mark.parametrize('permission', permissions)
@pytest.mark.parametrize('username', users)
def test_visible_project(db, sites, permission, username):
    sites.activate('foo.com')

    user = User.objects.get(username=username)
    project = Project.objects.get(id=12)
    project.visibility.sites.add(Site.objects.get(id=2))

    result = user.has_perm(permission, project)

    if permission == 'projects.add_project':
        # all users can create projects
        allowed = users

    elif permission in (
        'projects.add_visibility_object',
        'projects.add_membership_object',
        'projects.change_visibility_object',
        'projects.delete_visibility_object'
    ):
        # all users who act as site managers
        allowed = ('admin', 'api', 'site', 'example-manager')

    elif permission in (
        'projects.delete_project_object',
        'projects.change_membership_object',
        'projects.delete_membership_object',
        'projects.view_invite_object',
        'projects.add_invite_object',
        'projects.change_invite_object',
        'projects.delete_invite_object',
    ):
        # all users who act as owners of the project
        allowed = ('owner', 'admin', 'api', 'site', 'example-manager')

    elif permission in (
        'projects.change_project_object',
        'projects.import_project_object',
        'projects.export_project_object',
        'projects.add_integration_object',
        'projects.change_integration_object',
        'projects.delete_integration_object',
        'projects.add_issue_object',
        'projects.delete_issue_object',
        'projects.add_snapshot_object',
        'projects.change_snapshot_object',
        'projects.delete_snapshot_object',
        'projects.rollback_snapshot_object',
        'projects.export_snapshot_object',
    ):
        # all users who act as managers of the project
        allowed = ('owner', 'admin', 'api', 'site', 'example-manager')

    elif permission in (
        'projects.change_project_progress_object',
        'projects.add_value_object',
        'projects.change_value_object',
        'projects.delete_value_object',
        'projects.change_issue_object'
    ):
        # all users who act as authors of the project
        allowed = ('owner', 'admin', 'api', 'site', 'example-manager')

    elif permission.startswith('projects.view'):
        # all users who can access the project
        allowed = users

    elif permission == 'projects.leave_project_object':
        # any project member, but the last owner
        allowed = ('admin', )  # TODO: check if admin can be removed

    else:
        allowed = []

    assert result == (username in allowed)
