from ..models import Integration, Issue, Membership, Project, Snapshot, Value


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
