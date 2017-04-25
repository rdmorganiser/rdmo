from __future__ import absolute_import
import rules


@rules.predicate
def is_project_member(user, project):
    return user in project.member


@rules.predicate
def is_project_owner(user, project):
    return user in project.owners


@rules.predicate
def is_project_manager(user, project):
    return user in project.managers


@rules.predicate
def is_project_author(user, project):
    return user in project.authors


@rules.predicate
def is_project_guest(user, project):
    return user in project.guests

is_project_manager_or_owner = is_project_manager | is_project_owner
is_project_author_or_manager_or_owner = is_project_author | is_project_manager | is_project_owner

rules.add_perm('projects.view_project_object', is_project_member)
rules.add_perm('projects.change_project_object', is_project_manager_or_owner)
rules.add_perm('projects.delete_project_object', is_project_owner)
rules.add_perm('projects.export_project_object', is_project_owner)

rules.add_perm('projects.add_membership_object', is_project_owner)
rules.add_perm('projects.change_membership_object', is_project_owner)
rules.add_perm('projects.delete_membership_object', is_project_owner)

rules.add_perm('projects.view_snapshot_object', is_project_member)
rules.add_perm('projects.add_snapshot_object', is_project_manager_or_owner)
rules.add_perm('projects.change_snapshot_object', is_project_manager_or_owner)
rules.add_perm('projects.rollback_snapshot_object', is_project_manager_or_owner)

rules.add_perm('projects.view_value_object', is_project_member)
rules.add_perm('projects.add_value_object', is_project_author_or_manager_or_owner)
rules.add_perm('projects.change_value_object', is_project_author_or_manager_or_owner)
rules.add_perm('projects.delete_value_object', is_project_author_or_manager_or_owner)
