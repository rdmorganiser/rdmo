from ..models import Attribute


def test_attribute_str(db):
    instances = Attribute.objects.all()
    for instance in instances:
        assert str(instance)


def test_attribute_clean(db):
    instances = Attribute.objects.all()
    for instance in instances:
        instance.clean()
