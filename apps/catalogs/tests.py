from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils import translation

from .models import Catalog, Section, Subsection, Question, QuestionSet


class ClientTestCase(TestCase):
    fixtures = ['domain/testing.json', 'catalogs/testing.json']

    def setUp(self):
        translation.activate('en')


class ModelTestCase(TestCase):
    fixtures = ['domain/testing.json', 'catalogs/testing.json']

    def setUp(self):
        translation.activate('en')
        self.catalog = Catalog.objects.get(title_en="Catalog")
        self.section = Section.objects.get(title_en="Section")
        self.subsection = Subsection.objects.get(title_en="Subsection")
        self.question = Question.objects.get(text_en="Question")
        self.questionset = QuestionSet.objects.get(title_en="Question set")

    def test_catalog_str(self):
        string = self.catalog.title
        self.assertEqual(string, self.catalog.__str__())

    def test_section_str(self):
        string = '%s / %s' % (self.catalog.title, self.section.title)
        self.assertEqual(string, self.section.__str__())

    def test_subsection_str(self):
        string = '%s / %s / %s' % (self.catalog.title, self.section.title, self.subsection.title)
        self.assertEqual(string, self.subsection.__str__())

    def test_question_str(self):
        string = '%s / %s / %s / %s' % (self.catalog.title, self.section.title, self.subsection.title, self.question.text)
        self.assertEqual(string, self.question.__str__())

    def test_questionset_str(self):
        string = '%s / %s / %s / %s' % (self.catalog.title, self.section.title, self.subsection.title, self.questionset.title)
        self.assertEqual(string, self.questionset.__str__())
