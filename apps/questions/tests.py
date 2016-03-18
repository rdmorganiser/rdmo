from django.test import TestCase
from django.utils import translation

from apps.core.tests import TestListViewMixin, TestRetrieveViewMixin
from apps.core.tests import TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin
from apps.core.tests import TestModelStringMixin


from .models import Catalog, Section, Subsection, Question, QuestionSet


class QuestionsTestCase(TestCase):
    fixtures = ['accounts/testing.json', 'domain/testing.json', 'questions/testing.json']


class CatalogViewTests(TestListViewMixin, TestRetrieveViewMixin,
                       TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin,
                       TestModelStringMixin, QuestionsTestCase):

    list_url_name = 'catalogs'
    retrieve_url_name = 'catalog'

    create_url_name = 'catalog_create'
    update_url_name = 'catalog_update'
    delete_url_name = 'catalog_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.object = Catalog.objects.get(title_en='Catalog')


class SectionViewTests(TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin,
                       TestModelStringMixin, QuestionsTestCase):

    create_url_name = 'section_create'
    update_url_name = 'section_update'
    delete_url_name = 'section_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.object = Section.objects.get(title_en='Section')


class SubsectionViewTests(TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin,
                          TestModelStringMixin, QuestionsTestCase):

    create_url_name = 'subsection_create'
    update_url_name = 'subsection_update'
    delete_url_name = 'subsection_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.object = Subsection.objects.get(title_en='Subsection')


class QuestionViewTests(TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin,
                        TestModelStringMixin, QuestionsTestCase):

    create_url_name = 'question_create'
    update_url_name = 'question_update'
    delete_url_name = 'question_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.object = Question.objects.get(text_en='Question')


class QuestionSetQuestionViewTests(TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin,
                                   TestModelStringMixin, QuestionsTestCase):

    create_url_name = 'question_create'
    update_url_name = 'question_update'
    delete_url_name = 'question_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.object = Question.objects.get(text_en='Questionset Question')


class QuestionSetViewTests(TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin,
                           TestModelStringMixin, QuestionsTestCase):

    create_url_name = 'questionset_create'
    update_url_name = 'questionset_update'
    delete_url_name = 'questionset_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.object = QuestionSet.objects.get(title_en='Question set')
