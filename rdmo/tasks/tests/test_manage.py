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

    compare_import_to_export_data = True
    compare_import_to_export_ignore_list = []
    export_api = 'tasks_export'
    export_api_kwargs = {'format': 'xml'}
    export_api_format_list = ['pdf', 'rtf', 'odt', 'docx', 'html', 'markdown', 'mediawiki', 'tex', 'xml']
