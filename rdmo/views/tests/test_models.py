from ..models import View


def test_view_str(db):
    instances = View.objects.all()
    for instance in instances:
        assert str(instance)


def test_view_clean(db):
    instances = View.objects.all()
    for instance in instances:
        instance.clean()


def test_view_copy(db):
    instances = View.objects.all()
    for instance in instances:
        new_uri_prefix = instance.uri_prefix + '-'
        new_key = instance.key + '-'
        new_instance = instance.copy(new_uri_prefix, new_key)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.key == new_key
        assert list(new_instance.catalogs.values('id')) == list(new_instance.catalogs.values('id'))
        assert list(new_instance.sites.values('id')) == list(new_instance.sites.values('id'))
        assert list(new_instance.groups.values('id')) == list(new_instance.groups.values('id'))
