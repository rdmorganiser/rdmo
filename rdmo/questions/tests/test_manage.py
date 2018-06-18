from django.test import TestCase

from rdmo.core.testing.mixins import TestImportManageMixin


class QuestionsManageTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
        'questions.json',
    )


class ViewsImportManageTests(TestImportManageMixin, QuestionsManageTestCase):

    import_file = 'testing/xml/catalog.xml'
    export_api = 'questions_catalog_export'
    export_api_kwargs = {'format': 'xml', 'pk': '1'}
