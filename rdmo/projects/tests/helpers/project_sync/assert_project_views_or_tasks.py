import logging
from typing import Union

from rdmo.projects.handlers.utils import get_related_field_name_on_model_for_instance
from rdmo.projects.models import Project
from rdmo.tasks.models import Task
from rdmo.views.models import View

logger = logging.getLogger(__name__)


def assert_other_projects_unchanged(other_projects, initial_tasks_state):
    for other_project in other_projects:
        assert set(other_project.tasks.values_list('id', flat=True)) == set(initial_tasks_state[other_project.id])


def assert_all_projects_are_synced_with_instance_m2m_field(instance: Union[Task, View], field: str) -> None:
    # View/Task .catalogs, .sites or .groups
    instance_field = getattr(instance, field)
    instance_ids = set(instance_field.values_list('id', flat=True))
    # Project .catalog, .site or .groups
    instance_project_field = get_related_field_name_on_model_for_instance(Project, instance_field.model)
    # Project tasks or views
    m2m_field = get_related_field_name_on_model_for_instance(Project, instance)

    for project in Project.objects.all():
        # Project tasks or views
        project_instances = getattr(project, m2m_field).all()

        if not instance_ids:
            if instance not in project_instances:
                logger.debug(
                    '%s missing in %s when no %s are set [%s]',
                    instance,
                    instance_project_field,
                    project,
                    m2m_field
                )
            assert instance in project_instances, f"{instance} missing in {project} with matching {instance_project_field}"  # noqa: E501
            return

        if instance_project_field in ['site', 'catalog']:
            project_has_instance = getattr(project, instance_project_field).id in instance_ids
        elif instance_project_field in ['groups']:
            project_groups_ids = {i.id for i in getattr(project, instance_project_field)}
            project_has_instance = bool((project_groups_ids <= instance_ids) and project_groups_ids)

        if project_has_instance:
            if instance not in project_instances:
                logger.debug(
                    '%s missing in %s with %s match [%s]',
                    instance,
                    instance_project_field,
                    project,
                    m2m_field
                )
            assert instance in project_instances, f"{instance} missing in {project} with matching {instance_project_field}"  # noqa: E501
        else:
            if instance in project_instances:
                logger.debug(
                    '%s wrongly assigned to %s with %s mismatch [%s]',
                    instance,
                    instance_project_field,
                    project,
                    m2m_field
                )
            assert instance not in project_instances, f"{instance} wrongly assigned to {project} with mismatched {instance_project_field}"  # noqa: E501
