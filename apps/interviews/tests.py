from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import translation

from apps.projects.models import Project

from .models import Interview, Section, Subsection, Question, Jump, Answer


class ClientTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'password')
        self.project = Project(
            name='Test',
            pi='Tom Test',
            description='This is a Test.'
        )
        self.project.save()
        self.project.owner.add(self.user)
        self.project.save()

        self.interview = Interview(project=self.project, title='Title')
        self.interview.save()

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
        url = reverse('interview_create')

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
        self.user = User.objects.create_user('test', 'test@example.com', 'test')

        self.project = Project(name='Test', pi='Tom Test', description='This is a Test.')
        self.project.save()
        self.project.owner.add(self.user)
        self.project.save()

        self.interview = Interview(project=self.project, title='Title')
        self.interview.save()

        self.section = Section(slug='test_section', order=1, title_en='Test', title_de='Test')
        self.section.save()

        self.subsection = Subsection(slug='test_subsection', order=1, title_en='Test', title_de='Test', section=self.section)
        self.subsection.save()

        self.question = Question(slug='test_question', text_en='Test', text_de='Test', answer_type='text', widget_type='text', subsection=self.subsection)
        self.question.save()

        self.answer = Answer(interview=self.interview, question=self.question, value='Test')
        self.answer.save()

    def test_interview_str(self):
        self.assertEqual(self.interview.title, self.interview.__str__())

    def test_topic_str(self):
        self.assertEqual(self.section.slug, self.section.__str__())

    def test_catergory_str(self):
        self.assertEqual(self.section.slug + '.' + self.subsection.slug, self.subsection.__str__())

    def test_question_str(self):
        self.assertEqual(self.section.slug + '.' + self.subsection.slug + '.' + self.question.slug, self.question.__str__())

    def test_answer_str(self):
        self.assertEqual(self.question.slug, self.answer.__str__())
