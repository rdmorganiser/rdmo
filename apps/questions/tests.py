from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import translation

from .models import *


def questions_setUp(test_case):
    test_case.section = Section(
        slug='test_section',
        order=1,
        title_en='Test',
        title_de='Test'
    )
    test_case.section.save()

    test_case.subsection = Subsection(
        slug='test_subsection',
        order=1,
        title_en='Test',
        title_de='Test',
        section=test_case.section
    )
    test_case.subsection.save()

    test_case.group = Group(
        slug='test_group',
        title_en='Test',
        title_de='Test',
        subsection=test_case.subsection
    )
    test_case.group.save()

    test_case.question = Question(
        slug='test_question',
        text_en='Test',
        text_de='Test',
        answer_type='text',
        widget_type='text',
        group=test_case.group
    )
    test_case.question.save()


class ClientTestCase(TestCase):

    def setUp(self):
        translation.activate('en')


class ModelTestCase(TestCase):

    def setUp(self):
        questions_setUp(self)

    def test_section_str(self):
        self.assertEqual('Test', self.section.__str__())

    def test_subsection_str(self):
        self.assertEqual('Test / Test', self.subsection.__str__())

    def test_group_str(self):
        self.assertEqual('Test / Test / Test', self.group.__str__())

    def test_question_str(self):
        self.assertEqual('Test / Test / Test / Test', self.question.__str__())
