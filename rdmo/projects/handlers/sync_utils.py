import logging

from rdmo.projects.handlers.utils import get_related_field_name_on_model_for_instance
from rdmo.projects.models import Project

logger = logging.getLogger(__name__)


def sync_task_or_view_to_projects(instance):
    """Ensure the instance is linked to exactly the correct set of projects."""
    project_m2m_field = get_related_field_name_on_model_for_instance(Project, instance)
    target_projects = Project.objects.filter_projects_for_task_or_view(instance)

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
            'Removing %s from %s(id=%s).%s [sync_instance_to_projects]',
            instance,
            project,
            project.id,
            project_m2m_field
        )
        getattr(project, project_m2m_field).remove(instance)

    for project in to_add:
        logger.debug(
            'Adding %s to %s(id=%s).%s [sync_instance_to_projects]',
            instance,
            project,
            project.id,
            project_m2m_field
        )
        getattr(project, project_m2m_field).add(instance)


def sync_tasks_or_views_on_a_project(project, model):
    """Ensure the project is linked to exactly the correct instances of a model (View/Task)."""
    project_m2m_field = get_related_field_name_on_model_for_instance(Project, model)

    desired_instances = model.objects.filter_for_project(project)
    current_instances = getattr(project, project_m2m_field).all()

    to_remove = current_instances.exclude(pk__in=desired_instances)
    to_add = desired_instances.exclude(pk__in=current_instances)

    if not to_remove and not to_add:
        logger.debug(
            'Nothing to change for %s (%s) [sync_tasks_or_views_on_a_project]',
            project,
            project_m2m_field
        )
        return

    for instance in to_remove:
        logger.debug(
            'Removing %s from %s(id=%s).%s [sync_tasks_or_views_on_a_project]',
            instance,
            project,
            project.id,
            project_m2m_field
        )
        getattr(project, project_m2m_field).remove(instance)

    for instance in to_add:
        logger.debug(
            'Adding %s to %s(id=%s).%s [sync_tasks_or_views_on_a_project]',
            instance,
            project,
            project.id,
            project_m2m_field
        )
        getattr(project, project_m2m_field).add(instance)
