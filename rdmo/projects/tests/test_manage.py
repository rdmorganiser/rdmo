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
