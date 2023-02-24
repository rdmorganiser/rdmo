from django.contrib.sites.models import Site
from ..models import Condition


def test_condition_copy(db):
    instances = Condition.objects.all()
    current_site = Site.objects.get_current()
    foo_site, _created = Site.objects.get_or_create(domain='foo.com', name='foo.com')
    
    for instance in instances:
        instance.editors.set([foo_site])
        new_uri_prefix = instance.uri_prefix + '-'
        new_key = instance.key + '-'
        new_instance = instance.copy(new_uri_prefix, new_key)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.key == new_key
        assert new_instance.source == instance.source
        assert new_instance.target_option == instance.target_option
        # assertions for copy of editors
        assert new_instance.editors.count() == 1
        assert new_instance.editors.filter(id=current_site.id).exists() == True
        assert new_instance.editors.filter(id=foo_site.id).exists() == False
