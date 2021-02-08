import pytest

from ..models import Integration, Issue, Membership, Project, Snapshot, Value

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
