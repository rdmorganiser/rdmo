from ..models import Condition


def test_condition_str(db):
    instances = Condition.objects.all()
    for instance in instances:
        assert str(instance)


def test_condition_clean(db):
    instances = Condition.objects.all()
    for instance in instances:
        instance.clean()


def test_condition_copy(db):
    instances = Condition.objects.all()
    for instance in instances:
        new_uri_prefix = instance.uri_prefix + '-'
        new_key = instance.key + '-'
        new_instance = instance.copy(new_uri_prefix, new_key)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.key == new_key
        assert new_instance.source == instance.source
        assert new_instance.target_option == instance.target_option
