import os

from rdmo.core.xml import flat_xml_to_elements, read_xml_file
from rdmo.domain.models import Attribute
from rdmo.management.imports import import_elements
from rdmo.options.models import Option


def test_non_unique_path(db, settings):
    count = Attribute.objects.count()

    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'domain-non-unique-path.xml')
    root = read_xml_file(xml_file)
    elements = flat_xml_to_elements(root)
    checked = {element.get('uri'): True for element in elements}
    instances = import_elements(elements, parents={}, save=checked)

    # one instance has an error
    assert len([instance.errors for instance in instances.values() if instance.errors]) == 1

    # two instances have no error
    assert len([instance.errors for instance in instances.values() if not instance.errors]) == 2

    # only 2 attributes have been imported
    assert Attribute.objects.count() == count + 2


def test_non_unique_key(db, settings):
    count = Option.objects.count()

    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'options-non-unique-key.xml')
    root = read_xml_file(xml_file)
    elements = flat_xml_to_elements(root)
    checked = {element.get('uri'): True for element in elements}
    instances = import_elements(elements, parents={}, save=checked)

    # one instance has an error
    assert len([instance.errors for instance in instances.values() if instance.errors]) == 1

    # one instance has no error
    assert len([instance.errors for instance in instances.values() if not instance.errors]) == 1

    # no option has been imported
    assert Option.objects.count() == count


def test_missing_parent(db, settings):
    count = Option.objects.count()

    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'options-missing-parent.xml')
    root = read_xml_file(xml_file)
    elements = flat_xml_to_elements(root)
    checked = {element.get('uri'): True for element in elements}
    instances = import_elements(elements, parents={}, save=checked)

    # one instance has an error
    assert len([instance.errors for instance in instances.values() if instance.errors]) == 1

    # no option has been imported
    assert Option.objects.count() == count
