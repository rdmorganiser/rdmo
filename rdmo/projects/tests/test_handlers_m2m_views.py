from django.contrib.auth.models import Group

from rdmo.projects.models import Project
from rdmo.questions.models import Catalog
from rdmo.views.models import View

from .helpers import enable_project_views_sync  # noqa: F401

project_id = 10
view_id = 3
group_name = 'view_test'

def test_project_views_sync_when_adding_or_removing_a_catalog_to_or_from_a_view(
        db, settings, enable_project_views_sync  # noqa:F811
    ):
    assert settings.PROJECT_VIEWS_SYNC

    # Setup: Create a catalog, a view, and a project using the catalog
    project = Project.objects.get(id=project_id)
    catalog = project.catalog
    view = View.objects.get(id=view_id) # this view does not have catalogs in fixture
    # clearing the catalogs from the view adds the view to the catalog again
    view.catalogs.clear()
    # so the project.views are simply cleared here
    project.views.clear()
    initial_project_views = project.views.values_list('id', flat=True)

    # # Initially, the project should not have the view
    assert view not in project.views.all()

    ## Tests for .add and .remove
    # Add the catalog to the view and assert that the project now includes the view
    view.catalogs.add(catalog)
    assert view in project.views.all()

    # Remove the catalog from the view and assert that the project should no longer include the view
    view.catalogs.remove(catalog)
    if view.catalogs.exists():
        assert view not in project.views.all()
    else:
        assert view in project.views.all()

    ## Tests for .set and .clear
    # Add the catalog to the view and assert that the project now includes the view
    view.catalogs.set([catalog])
    assert view in project.views.all()

    # Remove the catalog from the view and assert that the project should no longer include the view
    view.catalogs.clear()
    assert view in project.views.all()

    # assert that the initial project views are unchanged
    assert set(project.views.values_list('id', flat=True)) == set(initial_project_views)

def test_project_views_sync_for_view_sites(
        db, settings, enable_project_views_sync  # noqa:F811
    ):
    assert settings.PROJECT_VIEWS_SYNC

    # Setup: Get an existing project and its associated site and create a view
    project = Project.objects.get(id=project_id)
    site = project.site
    view = View.objects.get(id=view_id)  # This view does not have sites in the fixture
    view.sites.clear()  # Ensure the view starts without any sites
    project.views.clear()
    initial_project_views = project.views.values_list('id', flat=True)

    # Ensure initial state: The project should not have the view
    assert view not in project.views.all()

    ## Tests for .add and .remove
    # Add the site to the view and assert that the project now includes the view
    view.sites.add(site)
    assert view in project.views.all()

    # Remove the site from the view, now the view has no sites so it is available to all
    view.sites.remove(site)
    assert not view.sites.exists()
    assert view in project.views.all()

    ## Tests for .set and .clear
    # Add the site to the view and assert that the project now includes the view
    view.sites.set([site])
    assert view in project.views.all()

    # Clear all sites from the view and assert that the project should no longer include the view
    view.sites.clear()
    assert view in project.views.all()

    # Assert that the initial project views are unchanged
    assert set(project.views.values_list('id', flat=True)) == set(initial_project_views)


def test_project_views_sync_when_adding_or_removing_a_group_to_or_from_a_view(
        db, settings, enable_project_views_sync  # noqa:F811
    ):
    assert settings.PROJECT_VIEWS_SYNC

    # Setup: Get an existing project, its associated group, and create a view
    project = Project.objects.get(id=project_id)
    user = project.owners.first()  # Get the first user associated with the project
    group = Group.objects.filter(name=group_name).first() # Get the first group the user belongs to
    user.groups.add(group)
    view = View.objects.get(id=view_id)  # This view does not have groups in the fixture
    view.groups.clear()  # Ensure the view starts without any groups
    project.views.clear()
    initial_project_views = project.views.values_list('id', flat=True)

    # Ensure initial state: The project should not have the view
    assert view not in project.views.all()

    ## Tests for .add and .remove
    # Add the group to the view and assert that the project now includes the view
    view.groups.add(group)
    assert view in project.views.all()

    # Remove the group from the view and assert that the project should no longer include the view
    view.groups.remove(group)
    if view.groups.exists():
        assert view in project.views.all()
    else:
        assert view not in project.views.all()

    ## Tests for .set and .clear
    # Add the group to the view and assert that the project now includes the view
    view.groups.set([group])
    assert view in project.views.all()

    # Clear all groups from the view and assert that the project should no longer include the view
    view.groups.clear()
    assert view in project.views.all()

    # Assert that the initial project views are unchanged
    assert set(project.views.values_list('id', flat=True)) == set(initial_project_views)



def test_project_view_removed_when_view_catalog_set_to_other(db, settings, enable_project_views_sync):  # noqa:F811
    assert settings.PROJECT_VIEWS_SYNC

    project = Project.objects.get(id=project_id)
    project_catalog = project.catalog
    view = View.objects.get(id=view_id)

    # Step 1: Project has a view (simulate by adding it manually)
    project.views.add(view)
    assert view in project.views.all()

    # Step 2: The view did NOT have the catalog of the project assigned, but we set another catalog
    other_catalog = Catalog.objects.exclude(id=project_catalog.id).first()
    assert other_catalog is not None
    view.catalogs.set([other_catalog])  # view now only for other_catalog

    # Step 3: The project should NOT have the view anymore (if sync logic is correct)
    project.refresh_from_db()
    assert view not in project.views.all()
