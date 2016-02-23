from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from django.utils import translation

from apps.plans.tests import plans_setUp

from .models import *


def catalogs_setUp(test_case):
    plans_setUp(test_case)

    test_case.catalog = Catalog.objects.create(
        title_en='Test',
        title_de='Test'
    )
    test_case.section = Section.objects.create(
        order=1,
        title_en='Test',
        title_de='Test',
        catalog=test_case.catalog
    )
    test_case.subsection = Subsection.objects.create(
        order=1,
        title_en='Test',
        title_de='Test',
        section=test_case.section
    )
    test_case.question = Question.objects.create(
        order=1,
        text_en='Test',
        text_de='Test',
        widget_type='text',
        subsection=test_case.subsection,
        attribute=test_case.attribute
    )
    test_case.questionset = QuestionSet.objects.create(
        order=1,
        title_en='Test',
        title_de='Test',
        subsection=test_case.subsection,
        attributeset=test_case.attributeset
    )
    test_case.question_bool = Question.objects.create(
        order=1,
        text_en='Test',
        text_de='Test',
        attribute=test_case.attributeset.attributes.first(),
        questionset=test_case.questionset,
        subsection=test_case.subsection
    )


class ClientTestCase(TestCase):

    def setUp(self):
        catalogs_setUp(self)
        translation.activate('en')


class ModelTestCase(TestCase):

    def setUp(self):
        catalogs_setUp(self)
        translation.activate('en')

    def test_catalog_str(self):
        self.assertEqual('Test', self.catalog.__str__())

    def test_section_str(self):
        self.assertEqual('Test / Test', self.section.__str__())

    def test_subsection_str(self):
        self.assertEqual('Test / Test / Test', self.subsection.__str__())

    def test_question_str(self):
        self.assertEqual('Test / Test / Test', self.question.__str__())

    def test_questionset_str(self):
        self.assertEqual('Test / Test / Test', self.questionset.__str__())
