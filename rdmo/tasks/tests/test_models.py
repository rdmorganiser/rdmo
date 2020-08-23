from ..models import Task


def test_task_str(db):
    instances = Task.objects.all()
    for instance in instances:
        assert str(instance)


def test_task_clean(db):
    instances = Task.objects.all()
    for instance in instances:
        instance.clean()


def test_task_copy(db):
    instances = Task.objects.all()
    for instance in instances:
        new_uri_prefix = instance.uri_prefix + '-'
        new_key = instance.key + '-'
        new_instance = instance.copy(new_uri_prefix, new_key)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.key == new_key
        assert new_instance.start_attribute == instance.start_attribute
        assert new_instance.end_attribute == instance.end_attribute
        assert list(new_instance.sites.values('id')) == list(new_instance.sites.values('id'))
        assert list(new_instance.groups.values('id')) == list(new_instance.groups.values('id'))
        assert list(new_instance.conditions.values('id')) == list(new_instance.conditions.values('id'))
