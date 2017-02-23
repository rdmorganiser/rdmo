from __future__ import absolute_import
import rules


@rules.predicate
def is_project_member(user, project):
    return user in project.member


@rules.predicate
def is_project_admin(user, project):
    return user in project.admins


@rules.predicate
def is_project_manager(user, project):
    return user in project.managers


@rules.predicate
def is_project_author(user, project):
    return user in project.authors


@rules.predicate
def is_project_guest(user, project):
    return user in project.guests


rules.add_perm('projects_rules.view_project', is_project_member)
rules.add_perm('projects_rules.change_project', is_project_admin | is_project_manager)
rules.add_perm('projects_rules.delete_project', is_project_admin)

rules.add_perm('projects_rules.view_snapshot', is_project_member)
rules.add_perm('projects_rules.add_snapshot', is_project_admin | is_project_manager)
rules.add_perm('projects_rules.change_snapshot', is_project_admin | is_project_manager)
rules.add_perm('projects_rules.rollback_snapshot', is_project_admin | is_project_manager)

rules.add_perm('projects_rules.view_value', is_project_admin)
rules.add_perm('projects_rules.add_value', is_project_admin | is_project_manager | is_project_author)
rules.add_perm('projects_rules.change_value', is_project_admin | is_project_manager | is_project_author)
rules.add_perm('projects_rules.delete_value', is_project_admin | is_project_manager | is_project_author)
