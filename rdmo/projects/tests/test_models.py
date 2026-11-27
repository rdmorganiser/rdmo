import pytest

from rdmo.questions.models import Catalog

from ..models import Integration, Issue, Membership, Project, Snapshot, Value, Visibility

projects = [1, 2, 3, 4, 5]


def test_integration_str(db):
    instances = Integration.objects.all()
    for instance in instances:
        assert str(instance)


def test_issue_str(db):
    instances = Issue.objects.all()
    for instance in instances:
        assert str(instance)


def test_project_str(db):
    instances = Project.objects.all()
    for instance in instances:
        assert str(instance)


@pytest.mark.parametrize('catalog_field', ['catalog', 'catalog_id'])
@pytest.mark.parametrize('make_update_fields', [tuple, iter])
def test_project_save_catalog_clears_progress(db, catalog_field, make_update_fields):
    project = Project.objects.get(pk=1)
    replacement = Catalog.objects.get(uri_path='catalog2')
    project.progress_count, project.progress_total = 3, 5
    project.save()

    project.catalog = replacement
    project.save(update_fields=make_update_fields((catalog_field,)))
    project.refresh_from_db()

    assert project.catalog_id == replacement.pk
    assert project.progress_count is None
    assert project.progress_total is None


def test_project_save_same_catalog_keeps_progress(db):
    project = Project.objects.get(pk=1)
    project.progress_count, project.progress_total = 3, 5
    project.save()

    project.description = 'Updated description'
    project.save()
    project.refresh_from_db()

    assert project.description == 'Updated description'
    assert (project.progress_count, project.progress_total) == (3, 5)


@pytest.mark.parametrize('update_fields', [('description',), ()], ids=('description-only', 'no-fields'))
def test_project_save_without_catalog_field_keeps_progress(db, update_fields):
    project = Project.objects.get(pk=1)
    original_catalog_id = project.catalog_id
    original_description = project.description
    project.progress_count, project.progress_total = 3, 5
    project.save()

    project.catalog = Catalog.objects.get(uri_path='catalog2')
    project.description = 'Updated description'
    project.save(update_fields=update_fields)
    project.refresh_from_db()

    assert project.catalog_id == original_catalog_id
    assert (project.progress_count, project.progress_total) == (3, 5)
    assert project.description == ('Updated description' if update_fields else original_description)


def test_membership_str(db):
    instances = Membership.objects.all()
    for instance in instances:
        assert str(instance)


def test_snapshot_str(db):
    instances = Snapshot.objects.all()
    for instance in instances:
        assert str(instance)


def test_value_str(db):
    instances = Value.objects.all()
    for instance in instances:
        assert str(instance)


def test_visibility_str(db):
    instances = Visibility.objects.all()
    for instance in instances:
        assert str(instance)


@pytest.mark.parametrize('project_id', projects)
def test_project_delete(db, project_id):
    project = Project.objects.get(id=project_id)
    project_parent_id = project.parent_id if project.parent else None
    project_children = [child.id for child in project.get_children()]

    project.delete()

    for child_id in project_children:
        child = Project.objects.get(id=child_id)

        if project_parent_id is None:
            assert child.parent is None
        else:
            assert child.parent.id is project_parent_id
