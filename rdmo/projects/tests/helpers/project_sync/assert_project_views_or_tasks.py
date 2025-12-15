import logging

from django.conf import settings

from rdmo.projects.handlers.sync_utils import get_related_field_name_on_model_for_instance
from rdmo.projects.models import Project
from rdmo.tasks.models import Task
from rdmo.views.models import View

logger = logging.getLogger(__name__)


def assert_other_projects_unchanged(other_projects, initial_tasks_state):
    for other_project in other_projects:
        assert set(other_project.tasks.values_list('id', flat=True)) == set(initial_tasks_state[other_project.id])


def assert_all_projects_are_synced_with_instance_m2m_field(instance: Task | View, field: str) -> None:
    # View/Task .catalogs, .sites or .groups
    instance_field = getattr(instance, field)
    # Project .catalog, .site or .groups
    instance_project_field = get_related_field_name_on_model_for_instance(Project, instance_field.model)
    # Project tasks or views
    m2m_field = get_related_field_name_on_model_for_instance(Project, instance)

    for project in Project.objects.all():
        # Project tasks or views
        project_instances = getattr(project, m2m_field).all()
        project_has_instance = instance in project_instances

        # (e.g. Task/View has no catalogs / no sites / no groups)
        if not instance_field.exists():
            if instance_project_field == 'site' and settings.MULTISITE:
                # MULTISITE=True and no sites on the instance:
                project_should_have_instance = False
            else:
                # For catalogs and groups, and for sites when MULTISITE=False:
                #   empty field means "applies to all projects"
                project_should_have_instance = True
        else:
            if instance_project_field == 'catalog':
                project_should_have_instance = bool(project.catalog in instance_field.all())
            elif instance_project_field == 'site':
                project_should_have_instance = bool(project.site in instance_field.all())
            elif instance_project_field == 'groups':
                instance_ids = set(instance_field.values_list('id', flat=True))
                project_groups_ids = {group.id for group in getattr(project, instance_project_field)}
                # project must have at least one group and all must be within instance_ids
                project_should_have_instance = bool(project_groups_ids and project_groups_ids <= instance_ids)
            else:
                raise ValueError("Project field not recognized, should be 'site', 'catalog' or 'groups'")

        if project_should_have_instance:
            if not project_has_instance:
                logger.debug(
                    '%s missing in %s with %s match [%s]',
                    instance,
                    instance_project_field,
                    project,
                    m2m_field
                )
            assert project_has_instance, (
                f"{instance} missing in {project} with matching {instance_project_field}"
            )
        else:
            if project_has_instance:
                logger.debug(
                    '%s wrongly assigned to %s with %s mismatch [%s]',
                    instance,
                    instance_project_field,
                    project,
                    m2m_field
                )
            assert not project_has_instance, (
                f"{instance} wrongly assigned to {project} with mismatched {instance_project_field} [{m2m_field}] "
            )
