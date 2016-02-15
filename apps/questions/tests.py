from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import translation

from .models import *


class ClientTestCase(TestCase):

    def setUp(self):
        translation.activate('en')


class ModelTestCase(TestCase):

    def setUp(self):
        self.section = Section(
            slug='test_section',
            order=1,
            title_en='Test',
            title_de='Test'
        )
        self.section.save()

        self.subsection = Subsection(
            slug='test_subsection',
            order=1,
            title_en='Test',
            title_de='Test',
            section=self.section
        )
        self.subsection.save()

        self.group = Group(
            slug='test_group',
            title_en='Test',
            title_de='Test',
            subsection=self.subsection
        )
        self.question.save()

        self.question = Question(
            slug='test_question',
            text_en='Test',
            text_de='Test',
            answer_type='text',
            widget_type='text',
            subsection=self.group
        )
        self.question.save()

    def test_section_str(self):
        self.assertEqual('test_section', self.section.__str__())

    def test_subsection_str(self):
        self.assertEqual('test_section.test_subsection', self.subsection.__str__())

    def test_group_str(self):
        self.assertEqual('test_section.test_subsection.test_group', self.group.__str__())

    def test_question_str(self):
        self.assertEqual('test_section.test_subsection.test_group.question', self.question.__str__())
