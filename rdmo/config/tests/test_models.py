from ..models import Plugin


def test_plugin_str(db):
    instances = Plugin.objects.all()
    for instance in instances:
        assert str(instance)


def test_plugin_clean(db):
    instances = Plugin.objects.all()
    for instance in instances:
        instance.clean()
