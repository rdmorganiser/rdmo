from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site

from rdmo.projects.models import Membership, Project

from ...questions.models import Catalog
from .utils import add_instance_to_projects, remove_instance_from_projects


def m2m_catalogs_changed_projects_sync_signal_handler(action, pk_set, instance, project_field):
    """
    Update project relationships for m2m_changed signals.

    Args:
        action (str): The m2m_changed action (post_add, post_remove, post_clear).
        pk_set (set): The set of primary keys for the related model instances.
        instance (Model): The instance being updated (e.g., View or Task).
        project_field (str): The field on Project to update (e.g., 'views', 'tasks').
    """
    if action == 'post_remove' and pk_set:
        related_instances = Catalog.objects.filter(pk__in=pk_set)
        projects_to_change = Project.objects.filter_catalogs(catalogs=related_instances).filter(
            **{project_field: instance}
        )
        remove_instance_from_projects(projects_to_change, project_field, instance)

    elif action == 'post_clear':
        projects_to_change = Project.objects.filter(**{project_field: instance})
        remove_instance_from_projects(projects_to_change, project_field, instance)

    elif action == 'post_add' and pk_set:
        related_instances = Catalog.objects.filter(pk__in=pk_set)
        projects_to_change = Project.objects.filter_catalogs(catalogs=related_instances).exclude(
            **{project_field: instance}
        )
        add_instance_to_projects(projects_to_change, project_field, instance)


def m2m_sites_changed_projects_sync_signal_handler(action, pk_set, instance, project_field):
    """
    Synchronize Project relationships for m2m_changed signals triggered by site updates.

    Args:
        action (str): The m2m_changed action (post_add, post_remove, post_clear).
        pk_set (set): The set of primary keys for the related model instances.
        instance (Model): The instance being updated (e.g., View or Task).
        project_field (str): The field on Project to update (e.g., 'views', 'tasks').
    """
    if action == 'post_remove' and pk_set:
        related_sites = Site.objects.filter(pk__in=pk_set)
        catalogs = instance.catalogs.all()

        projects_to_change = Project.objects.filter_catalogs(catalogs=catalogs).filter(
            site__in=related_sites,
            **{project_field: instance}
        )
        remove_instance_from_projects(projects_to_change, project_field, instance)

    elif action == 'post_clear':
        projects_to_change = Project.objects.filter_catalogs().filter(**{project_field: instance})
        remove_instance_from_projects(projects_to_change, project_field, instance)

    elif action == 'post_add' and pk_set:
        related_sites = Site.objects.filter(pk__in=pk_set)
        catalogs = instance.catalogs.all()

        projects_to_change = Project.objects.filter_catalogs(catalogs=catalogs).filter(
            site__in=related_sites
        ).exclude(**{project_field: instance})
        add_instance_to_projects(projects_to_change, project_field, instance)


def m2m_groups_changed_projects_sync_signal_handler(action, pk_set, instance, project_field):
    """
    Synchronize Project relationships for m2m_changed signals triggered by group updates.

    Args:
        action (str): The m2m_changed action (post_add, post_remove, post_clear).
        pk_set (set): The set of primary keys for the related model instances.
        instance (Model): The instance being updated (e.g., View or Task).
        project_field (str): The field on Project to update (e.g., 'views', 'tasks').
    """
    if action == 'post_remove' and pk_set:
        related_groups = Group.objects.filter(pk__in=pk_set)
        users = User.objects.filter(groups__in=related_groups)
        memberships = Membership.objects.filter(role='owner', user__in=users).values_list('id', flat=True)
        catalogs = instance.catalogs.all()

        projects_to_change = Project.objects.filter_catalogs(catalogs=catalogs).filter(
            memberships__in=memberships,
            **{project_field: instance}
        )
        remove_instance_from_projects(projects_to_change, project_field, instance)

    elif action == 'post_clear':
        # Remove all linked projects regardless of catalogs
        projects_to_change = Project.objects.filter_catalogs().filter(**{project_field: instance})
        remove_instance_from_projects(projects_to_change, project_field, instance)

    elif action == 'post_add' and pk_set:
        related_groups = Group.objects.filter(pk__in=pk_set)
        users = User.objects.filter(groups__in=related_groups)
        memberships = Membership.objects.filter(role='owner', user__in=users).values_list('id', flat=True)
        catalogs = instance.catalogs.all()

        projects_to_change = Project.objects.filter_catalogs(catalogs=catalogs).filter(
            memberships__in=memberships
        ).exclude(**{project_field: instance})
        add_instance_to_projects(projects_to_change, project_field, instance)
