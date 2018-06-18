from django.test import TestCase

from rdmo.core.testing.mixins import TestImportManageMixin


class ProjectsManageTestCase(TestCase):

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
        'questions.json',
        'tasks.json',
        'views.json',
        'projects.json'
    )


class ProjectsImportManageTests(TestImportManageMixin, ProjectsManageTestCase):

    import_file = 'testing/xml/project.xml'
    import_user = 'user'

    compare_import_to_export_data = False
    compare_import_to_export_ignore_list = ['created', 'updated']
    export_api = 'project_export_xml'
    export_api_kwargs = {'pk': '1'}
