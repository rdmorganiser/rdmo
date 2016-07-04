from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import RequestContext, Template
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.utils import translation

from apps.accounts.testing.factories import UserFactory, ManagerFactory, AdminFactory

from .mixins import *


class CoreTests(TestCase):

    def setUp(self):
        translation.activate('en')

        UserFactory()
        ManagerFactory()
        AdminFactory()

    def test_home_view(self):
        """ The home page can be accessed. """

        # test as AnonymousUser
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # test as regular user
        self.client.login(username='user', password='user')
        response = self.client.get('/')
        self.assertRedirects(response, reverse('projects'))

        # test as manager
        self.client.login(username='user', password='user')
        response = self.client.get('/')
        self.assertRedirects(response, reverse('projects'))

        # test as admin
        self.client.login(username='user', password='user')
        response = self.client.get('/')
        self.assertRedirects(response, reverse('projects'))

    # def test_not_found(self):
    #     ''' The redirect when accessing a link in a non active language works. '''

    #     # get the login link in german
    #     translation.activate('de')
    #     url = reverse('')

    #     # switch back to english
    #     translation.activate('en')

    #     # get the url and check the redirection
    #     response = self.client.get(url)
    #     self.assertRedirects(response, url)

    #     # switch back to english
    #     translation.activate('en')

    #     # get the wrong url (without trailing slash) and check for 404
    #     response = self.client.get('/*')
    #     self.assertEqual(404, response.status_code)

    def test_i18n_switcher(self):
        ''' The i18n switcher works. '''

        # get the url to switch to german
        url = reverse('i18n_switcher', args=['de'])

        # switch to german and check if the header is there
        response = self.client.get(url, HTTP_REFERER='http://testserver/')
        self.assertEqual(302, response.status_code)
        self.assertIn('de', response['Content-Language'])

        # get the url to switch to english
        url = reverse('i18n_switcher', args=['en'])

        # switch to german and check if the header is there
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)
        self.assertIn('en', response['Content-Language'])


class CoreTagsTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.manager = ManagerFactory()
        self.admin = AdminFactory()

        self.request = RequestFactory().get('/')

    def test_login_link_anonymus(self):
        """ The login link is for the anonymus user. """

        # create a fake template
        template = "{% load core_tags %}{% login_link %}"

        # set the user to anonymus and render the login link
        self.request.user = AnonymousUser()
        context = RequestContext(self.request, {})
        rendered_template = Template(template).render(context)
        self.assertEqual('<a href="%s">Login</a>' % reverse('login'), rendered_template)

    def test_login_link_user(self):
        """ The login link is for the anonymus user. """

        # create a fake template
        template = "{% load core_tags %}{% login_link %}"

        # set the user to a real user and render the login link
        self.request.user = User.objects.get(username=self.user.username)
        context = RequestContext(self.request, {})
        rendered_template = Template(template).render(context)
        self.assertEqual('<a href="%s">Logout</a>' % reverse('logout'), rendered_template)

    def test_internal_link(self):
        """ Intenal links are rendered correctly. """
        # create a fake template with a name
        template = "{% load core_tags %}{% internal_link 'Home' 'home' %}"

        # render the link
        context = RequestContext(self.request, {})
        rendered_template = Template(template).render(context)
        self.assertEqual('<a href="%s">Home</a>' % reverse('home'), rendered_template)

    def test_internal_link_no_name(self):
        """ Intenal links without name are rendered correctly. """
        # create a fake template without a name
        template = "{% load core_tags %}{% internal_link None 'home' %}"

        # render the link
        context = RequestContext(self.request, {})
        rendered_template = Template(template).render(context)
        url = reverse('home')
        self.assertEqual('<a href="%s">%s</a>' % (url, url), rendered_template)

    def test_internal_link_permission(self):
        """ Intenal links without name are rendered correctly. """
        # create a fake template with a permission
        template = "{% load core_tags %}{% internal_link 'Home' 'home' permission='permission' %}"

        # render the link
        context = RequestContext(self.request, {})
        self.request.user = AnonymousUser()
        rendered_template = Template(template).render(context)
        self.assertEqual('', rendered_template)

    def test_internal_link_login_required_anonymus(self):
        """ Intenal links without name are rendered correctly. """
        # create a fake template with the login_required permission
        template = "{% load core_tags %}{% internal_link 'Home' 'home' permission='login_required' %}"

        # render the link with the anonymous user
        context = RequestContext(self.request, {})
        self.request.user = AnonymousUser()
        rendered_template = Template(template).render(context)
        self.assertEqual('', rendered_template)

    def test_internal_link_login_required_user(self):
        """ Intenal links without name are rendered correctly. """
        url = reverse('home')

        # create a fake template with the login_required permission
        template = "{% load core_tags %}{% internal_link 'Home' 'home' permission='login_required' %}"

        # render the link with a proper user
        context = RequestContext(self.request, {})
        self.request.user = User.objects.get(username='user')
        rendered_template = Template(template).render(context)
        self.assertEqual('<a href="%s">Home</a>' % url, rendered_template)

    def test_i18n_switcher(self):
        """ The language switcher is rendered correctly. """

        # create a fake template with a name
        template = "{% load core_tags %}{% i18n_switcher %}"

        # set a language
        translation.activate(settings.LANGUAGES[0][0])

        # render the link
        context = RequestContext(self.request, {})
        rendered_template = Template(template).render(context)
        for language in settings.LANGUAGES:
            if language == settings.LANGUAGES[0]:
                self.assertIn('<a href="/i18n/%s/"><u>%s</u></a>' % language, rendered_template)
            else:
                self.assertIn('<a href="/i18n/%s/">%s</a>' % language, rendered_template)
