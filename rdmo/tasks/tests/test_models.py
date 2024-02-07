from ..models import Task


def test_task_str(db):
    instances = Task.objects.all()
    for instance in instances:
        assert str(instance)


def test_task_clean(db):
    instances = Task.objects.all()
    for instance in instances:
        instance.clean()
