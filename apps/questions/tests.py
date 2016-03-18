from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import translation

from apps.core.tests import TestListViewMixin
from apps.core.tests import TestRetrieveViewMixin
from apps.core.tests import TestCreateViewMixin
from apps.core.tests import TestUpdateViewMixin
from apps.core.tests import TestDeleteViewMixin
from apps.core.tests import TestModelStringMixin

from .models import Catalog, Section, Subsection, QuestionEntity, Question, QuestionSet


class QuestionsTestCase(TestCase):
    fixtures = ['accounts/testing.json', 'domain/testing.json', 'questions/testing.json']


class CatalogTests(TestListViewMixin, TestRetrieveViewMixin,
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
        self.instance = Catalog.objects.get(title_en='Catalog')

    def test_catalog_create_section_view_get(self):
        url = reverse('catalog_create_section', args=[self.instance.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_catalog_create_section_view_post(self):
        section = Section.objects.get(title_en='Section')

        url = reverse('catalog_create_section', args=[self.instance.pk])
        response = self.client.post(url, self.model_to_dict(section))
        self.assertEqual(response.status_code, 302)


class SectionTests(TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin,
                   TestModelStringMixin, QuestionsTestCase):

    create_url_name = 'section_create'
    update_url_name = 'section_update'
    delete_url_name = 'section_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.instance = Section.objects.get(title_en='Section')

    def test_section_create_subsection_view_get(self):
        url = reverse('section_create_subsection', args=[self.instance.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_section_create_subsection_view_post(self):
        subsection = Subsection.objects.get(title_en='Subsection')

        url = reverse('section_create_subsection', args=[self.instance.pk])
        response = self.client.post(url, self.model_to_dict(subsection))
        self.assertEqual(response.status_code, 302)


class SubsectionTests(TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin,
                      TestModelStringMixin, QuestionsTestCase):

    create_url_name = 'subsection_create'
    update_url_name = 'subsection_update'
    delete_url_name = 'subsection_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.instance = Subsection.objects.get(title_en='Subsection')

    def test_subsection_create_question_view_get(self):
        url = reverse('subsection_create_question', args=[self.instance.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_subsection_create_question_view_post(self):
        question = Question.objects.get(text_en='Question')

        url = reverse('subsection_create_question', args=[self.instance.pk])
        response = self.client.post(url, self.model_to_dict(question))
        self.assertEqual(response.status_code, 302)

    def test_subsection_create_questionset_view_get(self):
        url = reverse('subsection_create_questionset', args=[self.instance.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_subsection_create_questionset_view_post(self):
        questionset = QuestionSet.objects.get(title_en='Questionset')

        url = reverse('subsection_create_questionset', args=[self.instance.pk])
        response = self.client.post(url, self.model_to_dict(questionset))
        self.assertEqual(response.status_code, 302)


class QuestionEntityQuestionTests(TestModelStringMixin, QuestionsTestCase):

    def setUp(self):
        translation.activate('en')
        question = Question.objects.get(text_en='Question')
        self.instance = QuestionEntity.objects.get(pk=question.pk)


class QuestionEntityQuestionSetTests(TestModelStringMixin, QuestionsTestCase):

    def setUp(self):
        translation.activate('en')
        questionset = QuestionSet.objects.get(title_en='Questionset')
        self.instance = QuestionEntity.objects.get(pk=questionset.pk)


class QuestionSetTests(TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin,
                       TestModelStringMixin, QuestionsTestCase):

    create_url_name = 'questionset_create'
    update_url_name = 'questionset_update'
    delete_url_name = 'questionset_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.instance = QuestionSet.objects.get(title_en='Questionset')

    def test_questionset_create_question_view_get(self):
        url = reverse('questionset_create_question', args=[self.instance.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_questionset_create_question_view_post(self):
        question = Question.objects.get(text_en='Question')

        url = reverse('questionset_create_question', args=[self.instance.pk])
        response = self.client.post(url, self.model_to_dict(question))
        self.assertEqual(response.status_code, 302)


class QuestionTests(TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin,
                    TestModelStringMixin, QuestionsTestCase):

    create_url_name = 'question_create'
    update_url_name = 'question_update'
    delete_url_name = 'question_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.instance = Question.objects.get(text_en='Question')


class QuestionSetQuestionTests(TestCreateViewMixin, TestUpdateViewMixin, TestDeleteViewMixin,
                               TestModelStringMixin, QuestionsTestCase):

    create_url_name = 'question_create'
    update_url_name = 'question_update'
    delete_url_name = 'question_delete'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='user', password='user')
        self.instance = Question.objects.get(text_en='Questionset Question')
