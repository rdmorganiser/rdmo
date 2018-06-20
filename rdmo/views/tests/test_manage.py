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

    compare_import_to_export_data = True
    compare_import_to_export_ignore_list = ['template']
    export_api = 'views_export'
    export_api_kwargs = {'format': 'xml'}
    export_api_format_list = ['pdf', 'rtf', 'odt', 'docx', 'html', 'markdown', 'mediawiki', 'tex', 'xml']
