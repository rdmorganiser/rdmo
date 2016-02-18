from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils import translation

from apps.projects.tests import projects_setUp
from apps.questions.tests import questions_setUp

from .models import Interview, Answer


def interviews_setUp(test_case):
    projects_setUp(test_case)

    test_case.interview = Interview.objects.create(
        project=test_case.project,
        title='test_title',
        completed=False
    )

    questions_setUp(test_case)

    test_case.answer = Answer.objects.create(
        interview=test_case.interview,
        question=test_case.question,
        value='test_value'
    )
    test_case.answer_yes = Answer.objects.create(
        interview=test_case.interview,
        question=test_case.question_bool,
        value='1'
    )
    test_case.answer_no = Answer.objects.create(
        interview=test_case.interview,
        question=test_case.question_bool,
        value='0'
    )


class ClientTestCase(TestCase):

    def setUp(self):
        interviews_setUp(self)
        translation.activate('en')

    def test_interview(self):
        """ The interview_create page can be accessed. """

        # get the url
        url = reverse('interview', args=[self.interview.pk])

        # get the client object and log in
        client = Client()
        client.login(username='user', password='password')

        # access the page
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_interview_create(self):
        """ The interview_create page can be accessed. """

        # get the url
        url = reverse('interview_create', args=[self.project.pk])

        # get the client object and log in
        client = Client()
        client.login(username='user', password='password')

        # access the page
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_interview_update(self):
        """ A project can be created. """

        # get the url
        url = reverse('interview_update', args=[self.interview.pk])

        # get the client object and log in
        client = Client()
        client.login(username='user', password='password')

        # access the page
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_interview_delete(self):
        """ A project can be created. """

        # get the url
        url = reverse('interview_delete', args=[self.interview.pk])

        # get the client object and log in
        client = Client()
        client.login(username='user', password='password')

        # access the page
        response = client.get(url)
        self.assertEqual(response.status_code, 200)


class ModelTestCase(TestCase):

    def setUp(self):
        interviews_setUp(self)
        translation.activate('en')

    def test_interview_str(self):
        self.assertEqual('test_title', self.interview.__str__())

    def test_answer_properties(self):
        self.assertEqual('test_value', self.answer.text)
        self.assertEqual('yes', self.answer_yes.text)
        self.assertEqual('no', self.answer_no.text)

        self.assertEqual('test_title', self.answer.project_title)
        self.assertEqual('test_title', self.answer.interview_title)
        self.assertEqual('test_section', self.answer.section_slug)
        self.assertEqual('test_subsection', self.answer.subsection_slug)
        self.assertEqual('test_group', self.answer.group_slug)
        self.assertEqual('test_question', self.answer.question_slug)

    def test_answer_str(self):
        self.assertEqual('test_question', self.answer.__str__())
