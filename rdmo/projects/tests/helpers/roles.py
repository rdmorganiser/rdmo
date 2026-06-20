from rdmo.projects.constants import ROLE_RANKS


def get_project_roles(project, project_ancestors, username):
    current_membership = project.memberships.filter(user__username=username).first()
    current_role = current_membership.role if current_membership else None

    highest_role = current_role
    for project_ancestor in project_ancestors:
        project_membership = project_ancestor.memberships.filter(user__username=username).first()
        if project_membership:
            if highest_role is None or ROLE_RANKS[highest_role] < ROLE_RANKS[project_membership.role]:
                highest_role = project_membership.role

    return current_role, highest_role
