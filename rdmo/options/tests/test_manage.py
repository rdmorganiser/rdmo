from django.test import TestCase

from rdmo.core.testing.mixins import TestImportManageMixin


class OptionsManageTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
    )


class OptionsImportManageTests(TestImportManageMixin, OptionsManageTestCase):

    import_file = 'testing/xml/catalog.xml'
