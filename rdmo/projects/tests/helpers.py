from collections import defaultdict

from rdmo.questions.models import Catalog
from rdmo.views.models import View


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
