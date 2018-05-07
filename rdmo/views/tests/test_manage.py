from django.test import TestCase

from rdmo.core.testing.mixins import TestImportManageMixin


class ViewsManageTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
        'views.json',
    )


class ViewsImportManageTests(TestImportManageMixin, ViewsManageTestCase):

    import_file = 'testing/xml/views.xml'
