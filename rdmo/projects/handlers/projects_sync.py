import logging

from rdmo.projects.handlers.utils import get_related_field_name_for_instance
from rdmo.projects.models import Project

logger = logging.getLogger(__name__)


def get_projects_to_be_synced(instance):
    """Return projects that should be linked to the given instance (View/Task)."""

    # when View or Task is not available, remove from all projects
    if not instance.available:
        return Project.objects.none()

    # filter projects wherein the catalog is not available
    projects = Project.objects.filter(catalog__available=True)

    if instance.catalogs.exists():
        projects = projects.filter(catalog__in=instance.catalogs.all())

    if instance.sites.exists():
        projects = projects.filter(site__in=instance.sites.all())

    if instance.groups.exists():
        projects = projects.filter_groups(instance.groups.all())

    return projects


def sync_instance_to_projects(instance):
    """Ensure the instance is linked to exactly the correct set of projects."""
    project_m2m_field = get_related_field_name_for_instance(Project, instance)
    target_projects = get_projects_to_be_synced(instance)

    current_projects = Project.objects.filter(**{project_m2m_field: instance})

    to_remove = current_projects.exclude(pk__in=target_projects)
    to_add = target_projects.exclude(pk__in=current_projects)
    if not to_remove and not to_add:
        logger.debug(
            'Nothing to change for %s (%s) [sync_instance_to_projects]',
            instance,
            project_m2m_field
        )
        return

    for project in to_remove:
        logger.debug(
            'Removing %s from %s (%s) [sync_instance_to_projects]',
            instance,
            project,
            project_m2m_field
        )
        getattr(project, project_m2m_field).remove(instance)

    for project in to_add:
        logger.debug(
            'Adding %s to %s (%s) [sync_instance_to_projects]',
            instance,
            project,
            project_m2m_field
        )
        getattr(project, project_m2m_field).add(instance)


def sync_project_instances(project, model):
    """Ensure the project is linked to exactly the correct instances of a model (View/Task)."""
    project_m2m_field = get_related_field_name_for_instance(Project, model)

    desired_instances = model.objects.filter_for_project(project).filter(available=True)
    current_instances = getattr(project, project_m2m_field).all()

    to_remove = current_instances.exclude(pk__in=desired_instances)
    for instance in to_remove:
        logger.debug(
            'Removing %s from %s (%s) [sync_project_instances]',
            instance,
            project,
            project_m2m_field
        )
        getattr(project, project_m2m_field).remove(instance)

    to_add = desired_instances.exclude(pk__in=current_instances)
    for instance in to_add:
        logger.debug(
            'Adding %s to %s (%s) [sync_project_instances]',
            instance,
            project,
            project_m2m_field
        )
        getattr(project, project_m2m_field).add(instance)
