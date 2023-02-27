
from django.contrib.sites.models import Site

from ..models import Attribute


def test_attribute_copy_editors(db):
    instances = Attribute.objects.all()
    for instance in instances:
        instance.editors.add(Site.objects.get_current())
        new_uri_prefix = instance.uri_prefix + '-'
        new_key = instance.key + '-'
        new_instance = instance.copy(new_uri_prefix, new_key)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.key == new_key
        assert new_instance.parent == instance.parent
        assert new_instance.get_descendants().count() == new_instance.get_descendants().count()
        #