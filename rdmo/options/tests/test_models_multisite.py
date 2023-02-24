from django.contrib.sites.models import Site

from ..models import Option, OptionSet


def test_optionset_copy_editors_currentsite(db):
    instances = OptionSet.objects.all()
    current_site = Site.objects.get_current()
    foo_site, _created = Site.objects.get_or_create(domain='foo.com', name='foo.com')

    for instance in instances:
        instance.editors.set([foo_site])
        new_uri_prefix = instance.uri_prefix + '-'
        new_key = instance.key + '-'
        new_instance = instance.copy(new_uri_prefix, new_key)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.key == new_key
        assert list(new_instance.conditions.values('id')) == list(new_instance.conditions.values('id'))
        assert new_instance.options.count() == instance.options.count()
        # assertions for copy of editors
        assert new_instance.editors.count() == 1
        assert new_instance.editors.filter(id=current_site.id).exists() == True
        assert new_instance.editors.filter(id=foo_site.id).exists() == False
        


def test_options_clean(db):
    instances = Option.objects.all()
    for instance in instances:
        instance.clean()


def test_options_copy_editors_currentsite(db):
    instances = Option.objects.all()
    current_site = Site.objects.get_current()
    foo_site, _created = Site.objects.get_or_create(domain='foo.com', name='foo.com')

    for instance in instances:
        instance.editors.set([foo_site])
        new_uri_prefix = instance.uri_prefix + '-'
        new_key = instance.key + '-'
        new_instance = instance.copy(new_uri_prefix, new_key)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.key == new_key
        # assertions for copy of editors
        assert new_instance.editors.count() == 1
        assert new_instance.editors.filter(id=current_site.id).exists() == True
        assert new_instance.editors.filter(id=foo_site.id).exists() == False

