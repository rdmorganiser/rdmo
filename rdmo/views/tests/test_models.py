from ..models import View


def test_view_str(db):
    instances = View.objects.all()
    for instance in instances:
        assert str(instance)


def test_view_clean(db):
    instances = View.objects.all()
    for instance in instances:
        instance.clean()
