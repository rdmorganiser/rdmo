import logging
from collections import defaultdict
from typing import Union

import pytest

from django.apps import apps

from rdmo.projects.handlers.utils import get_related_field_name_for_instance
from rdmo.projects.models import Project
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
from rdmo.views.models import View

logger = logging.getLogger(__name__)

@pytest.fixture
def enable_project_views_sync(settings):
    settings.PROJECT_VIEWS_SYNC = True
    apps.get_app_config('projects').ready()

@pytest.fixture
def enable_project_tasks_sync(settings):
    settings.PROJECT_TASKS_SYNC = True
    apps.get_app_config('projects').ready()

def assert_other_projects_unchanged(other_projects, initial_tasks_state):
    for other_project in other_projects:
        assert set(other_project.tasks.values_list('id', flat=True)) == set(initial_tasks_state[other_project.id])



def get_catalog_view_mapping():
    """
    Generate a mapping of catalogs to their associated views.
    Includes all catalogs, even those with no views, and adds `sites` and `groups` for each view.
    """
    # Initialize an empty dictionary for the catalog-to-views mapping
    catalog_views_mapping = defaultdict(list)

    # Populate the mapping for all catalogs
    for catalog in Catalog.objects.all():
        catalog_views_mapping[catalog.id] = []

    # Iterate through all views and enrich the mapping
    for view in View.objects.prefetch_related('sites', 'groups'):
        if view.catalogs.exists():  # Only include views with valid catalogs
            for catalog in view.catalogs.all():
                catalog_views_mapping[catalog.id].append({
                    'id': view.id,
                    'sites': list(view.sites.values_list('id', flat=True)),
                    'groups': list(view.groups.values_list('id', flat=True))
                })

    # Convert defaultdict to a regular dictionary
    return dict(catalog_views_mapping)


def assert_all_projects_are_synced_with_instance_m2m_field(instance: Union[Task, View], field: str) -> None:
    # View/Task .catalogs, .sites or .groups
    instance_ids = set(getattr(instance, field).values_list('id', flat=True))
    # Project .catalog, .site or .groups
    instance_project_field = get_related_field_name_for_instance(Project, getattr(instance, field).model)
    # Project tasks or views
    m2m_field = get_related_field_name_for_instance(Project, instance)


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
        else:
            if instance_project_field in ['site', 'catalog']:
                if getattr(project, instance_project_field).id in instance_ids:
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
            elif instance_project_field in ['groups']:
                if {i.id for i in getattr(project, instance_project_field)} <= instance_ids:
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




def _get_projects_views_state():
    """ currently not used """
    ret = {}
    one_two_three = (1, 2, 3)
    P_TITLE = "Sync P{}"
    for n in one_two_three:
        project = Project.objects.filter(title=P_TITLE.format(n)).first()
        p_state = {"C": project.catalog.id, "V": project.views.all().values_list('id', flat=True)}
        ret['P'][n] = p_state

        view = View.objects.get(id=n)
        v_state = {"C": view.catalogs.all().values_list('id', flat=True)}
        ret['V'][n] = v_state

        task = Task.objects.get(id=n)
        t_state = {"C": task.catalogs.all().values_list('id', flat=True)}
        ret['T'][n] = t_state

    return ret
