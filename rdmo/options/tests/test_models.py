from ..models import Option, OptionSet


def test_optionset_str(db):
    instances = OptionSet.objects.all()
    for instance in instances:
        assert str(instance)


def test_optionset_clean(db):
    instances = OptionSet.objects.all()
    for instance in instances:
        instance.clean()


def test_options_str(db):
    instances = Option.objects.all()
    for instance in instances:
        assert str(instance)


def test_optionset_copy(db):
    instances = OptionSet.objects.all()
    for instance in instances:
        new_uri_prefix = instance.uri_prefix + '-'
        new_key = instance.key + '-'
        new_instance = instance.copy(new_uri_prefix, new_key)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.key == new_key
        assert list(new_instance.conditions.values('id')) == list(new_instance.conditions.values('id'))
        assert new_instance.options.count() == instance.options.count()


def test_options_clean(db):
    instances = Option.objects.all()
    for instance in instances:
        instance.clean()


def test_options_copy(db):
    instances = Option.objects.all()
    for instance in instances:
        new_uri_prefix = instance.uri_prefix + '-'
        new_key = instance.key + '-'
        new_instance = instance.copy(new_uri_prefix, new_key)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.key == new_key
