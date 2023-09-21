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


def test_options_clean(db):
    instances = Option.objects.all()
    for instance in instances:
        instance.clean()
