from collections import defaultdict

from rdmo.projects.models import Project
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
from rdmo.views.models import View


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
            view_catalogs = view.catalogs.all()
        else:
            view_catalogs = Catalog.objects.all()

        for catalog in view_catalogs:
            catalog_views_mapping[catalog.id].append({
                'id': view.id,
                'available': view.available,
                'sites': list(view.sites.values_list('id', flat=True)),
                'groups': list(view.groups.values_list('id', flat=True))
            })

    # Convert defaultdict to a regular dictionary
    return dict(catalog_views_mapping)


def get_catalog_task_mapping():
    """
    Generate a mapping of catalogs to their associated tasks.
    Includes all catalogs, even those with no tasks, and adds `sites` and `groups` for each task.
    """
    # Initialize an empty dictionary for the catalog-to-tasks mapping
    catalog_tasks_mapping = defaultdict(list)

    # Populate the mapping for all catalogs
    for catalog in Catalog.objects.all():
        catalog_tasks_mapping[catalog.id] = []

    # Iterate through all tasks and enrich the mapping
    for task in Task.objects.prefetch_related('sites', 'groups'):
        if task.catalogs.exists():  # Only include tasks with valid catalogs
            task_catalogs = task.catalogs.all()
        else:
            task_catalogs = Catalog.objects.all()

        for catalog in task_catalogs:
            catalog_tasks_mapping[catalog.id].append({
                'id': task.id,
                'available': task.available,
                'sites': list(task.sites.values_list('id', flat=True)),
                'groups': list(task.groups.values_list('id', flat=True))
            })

    # Convert defaultdict to a regular dictionary
    return dict(catalog_tasks_mapping)



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
