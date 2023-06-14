import rules

from rules.predicates import is_authenticated


@rules.predicate
def is_project_member(user, project):
    if project is None: # needed for swagger
        return False
    return user in project.member or (project.parent and is_project_member(user, project.parent))


@rules.predicate
def is_current_project_member(user, project):
    return user in project.member


@rules.predicate
def is_project_owner(user, project):
    if project is None: # needed for swagger
        return False
    return user in project.owners or (project.parent and is_project_owner(user, project.parent))


@rules.predicate
def is_project_manager(user, project):
    if project is None: # needed for swagger
        return False
    return user in project.managers or (project.parent and is_project_manager(user, project.parent))


@rules.predicate
def is_project_author(user, project):
    if project is None: # needed for swagger
        return False
    return user in project.authors or (project.parent and is_project_author(user, project.parent))


@rules.predicate
def is_project_guest(user, project):
    if project is None: # needed for swagger
        return False
    return user in project.guests or (project.parent and is_project_guest(user, project.parent))


@rules.predicate
def is_site_manager(user, project):
    if project is None: # needed for swagger
        return False
    if user.is_authenticated:
        return user.role.manager.filter(pk=project.site.pk).exists()
    else:
        return False

# Users that can add projects
rules.add_perm('projects.add_project_object', is_authenticated)

rules.add_perm('projects.view_project_object', is_project_member | is_site_manager)
rules.add_perm('projects.change_project_object', is_project_manager | is_project_owner | is_site_manager)
rules.add_perm('projects.delete_project_object', is_project_owner | is_site_manager)
rules.add_perm('projects.leave_project_object', is_current_project_member)
rules.add_perm('projects.export_project_object', is_project_owner | is_project_manager | is_site_manager)
rules.add_perm('projects.import_project_object', is_project_owner | is_project_manager | is_site_manager)

rules.add_perm('projects.view_membership_object', is_project_member | is_site_manager)
rules.add_perm('projects.add_membership_object', is_project_owner | is_site_manager)
rules.add_perm('projects.change_membership_object', is_project_owner | is_site_manager)
rules.add_perm('projects.delete_membership_object', is_project_owner | is_site_manager)

rules.add_perm('projects.view_invite_object', is_project_owner | is_site_manager)
rules.add_perm('projects.add_invite_object', is_project_owner | is_site_manager)
rules.add_perm('projects.change_invite_object', is_project_owner | is_site_manager)
rules.add_perm('projects.delete_invite_object', is_project_owner | is_site_manager)

rules.add_perm('projects.view_integration_object', is_project_member | is_site_manager)
rules.add_perm('projects.add_integration_object', is_project_owner | is_project_manager | is_site_manager)
rules.add_perm('projects.change_integration_object', is_project_owner | is_project_manager | is_site_manager)
rules.add_perm('projects.delete_integration_object', is_project_owner | is_project_manager | is_site_manager)

rules.add_perm('projects.view_issue_object', is_project_member | is_site_manager)
rules.add_perm('projects.add_issue_object', is_project_manager | is_project_owner | is_site_manager)
rules.add_perm('projects.change_issue_object', is_project_author | is_project_manager | is_project_owner | is_site_manager)
rules.add_perm('projects.delete_issue_object', is_project_manager | is_project_owner | is_site_manager)

rules.add_perm('projects.view_snapshot_object', is_project_member | is_site_manager)
rules.add_perm('projects.add_snapshot_object', is_project_manager | is_project_owner | is_site_manager)
rules.add_perm('projects.change_snapshot_object', is_project_manager | is_project_owner | is_site_manager)
rules.add_perm('projects.rollback_snapshot_object', is_project_manager | is_project_owner | is_site_manager)

rules.add_perm('projects.view_value_object', is_project_member | is_site_manager)
rules.add_perm('projects.add_value_object', is_project_author | is_project_manager | is_project_owner | is_site_manager)
rules.add_perm('projects.change_value_object', is_project_author | is_project_manager | is_project_owner | is_site_manager)
rules.add_perm('projects.delete_value_object', is_project_author | is_project_manager | is_project_owner | is_site_manager)

rules.add_perm('questions.view_page_object', is_project_member | is_site_manager)

# TODO: use one of the permissions above
rules.add_perm('projects.is_project_owner', is_project_owner)
