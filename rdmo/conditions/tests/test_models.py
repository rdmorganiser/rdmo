from ..models import Condition


def test_condition_str(db):
    instances = Condition.objects.all()
    for instance in instances:
        assert str(instance)


def test_condition_clean(db):
    instances = Condition.objects.all()
    for instance in instances:
        instance.clean()
