from django.test import TestCase

from rdmo.core.testing.mixins import TestImportManageMixin


class TasksManageTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
        'tasks.json',
    )


class ViewsImportManageTests(TestImportManageMixin, TasksManageTestCase):

    import_file = 'testing/xml/tasks.xml'
