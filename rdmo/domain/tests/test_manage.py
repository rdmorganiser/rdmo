from django.test import TestCase

from rdmo.core.testing.mixins import TestImportManageMixin


class DomainManageTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
    )


class DomainImportManageTests(TestImportManageMixin, DomainManageTestCase):

    import_file = 'testing/xml/domain.xml'
