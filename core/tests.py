import re

from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.template import Context, RequestContext, Template
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import Site
from django.utils import translation


class ClientTestCase(TestCase):

    def setUp(self):
        User.objects.create_user('user', 'user@example.com', 'password')
        User.objects.create_superuser('admin', 'admin@example.com', 'password')
        translation.activate('en')

    def test_home(self):
        """ The home page can be accessed. """

        # get the client object
        client = Client()

        # test as AnonymousUser
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

        # test as regular user
        client.login(username='user', password='password')
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

        # test as superuser
        client.login(username='admin', password='password')
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_password_change(self):
        """ The user can change his/her password. """

        # get the client object
        client = Client()

        # try without being logged in
        response = client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 302)

        # log in
        client.login(username='user', password='password')

        # try again
        response = client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)

        # post an invalid form
        response = client.post(reverse('password_change'), {
            'old_password': 'drowssap',
            'new_password1': 'drowssap',
            'new_password2': 'drowssap'
        })
        self.assertEqual(response.status_code, 200)

        # post a valid form
        response = client.post(reverse('password_change'), {
            'old_password': 'password',
            'new_password1': 'drowssap',
            'new_password2': 'drowssap'
        })
        self.assertRedirects(response, reverse('password_change_done'))

    def test_password_reset(self):
        """ The user can rest his/her password if he/she forgot. """

        # get the client object
        client = Client()

        # get the password_reset page
        response = client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

        # post an invalid email
        response = client.post(reverse('password_reset'), {
            'email': 'wrong@example.com'
        })
        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 0)

        # post a valid email
        response = client.post(reverse('password_reset'), {
            'email': 'user@example.com'
        })
        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)

        # get the link from the mail
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mail.outbox[0].body)
        self.assertEqual(len(urls), 1)

        # get the password_reset page
        response = client.get(urls[0])
        self.assertEqual(response.status_code, 200)

        # post an invalid form
        response = client.post(urls[0], {
            'new_password1': 'password',
            'new_password2': 'drowssap'
        })
        self.assertEqual(response.status_code, 200)

        # post a valid form
        response = client.post(urls[0], {
            'new_password1': 'drowssap',
            'new_password2': 'drowssap'
        })
        self.assertRedirects(response, reverse('password_reset_complete'))

        # log in
        response = client.login(username='user', password='drowssap')
        self.assertTrue(response)

    def test_not_found(self):
        ''' The redirect when accessing a link in a non active language works. '''

        # get the client object
        client = Client()

        # get the login link in german
        translation.activate('de')
        url = reverse('login')

        # switch back to english
        translation.activate('en')

        # get the url and check the redirection
        response = client.get(url)
        self.assertRedirects(response, url)

        # switch back to english
        translation.activate('en')

        # get the wrong url (without trailing slash) and check for 404
        response = client.get('/*')
        self.assertEqual(404, response.status_code)

    def test_i18n_switcher(self):
        ''' The i18n switcher works. '''

        # get the client object
        client = Client()

        # get the url to switch to german
        url = reverse('i18n_switcher', args=['de'])

        # switch to german and check if the header is there
        response = client.get(url, HTTP_REFERER='http://testserver/')
        self.assertEqual(302, response.status_code)
        self.assertIn('de', response['Content-Language'])

        # get the url to switch to english
        url = reverse('i18n_switcher', args=['en'])

        # switch to german and check if the header is there
        response = client.get(url)
        self.assertEqual(302, response.status_code)
        self.assertIn('en', response['Content-Language'])


class TemplateTagsTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        self.user = User.objects.create_user('user', 'user@example.com', 'password')

        # set up a site with an alias
        site = Site.objects.get_current()
        site.domain = 'example.com'
        site.save()

    def test_login_link(self):
        """ The login link is rendered correctly. """

        # create a fake template
        template = "{% load core_tags %}{% login_link %}"

        # set the user to anonymus and render the login link
        self.request.user = AnonymousUser()
        context = RequestContext(self.request, {})
        rendered_template = Template(template).render(context)
        self.assertEqual('<a href="%s">Login</a>' % reverse('login'), rendered_template)

        # set the user to a real user and render the login link
        self.request.user = self.user
        context = RequestContext(self.request, {})
        rendered_template = Template(template).render(context)
        self.assertEqual('<a href="%s">Logout</a>' % reverse('logout'), rendered_template)

    def test_internal_link(self):
        """ Intenal links are rendered correctly. """

        # get the url of the home page
        url = reverse('home')

        # create a fake template with a name
        template = "{% load core_tags %}{% internal_link 'home' 'Home' %}"

        # render the link
        context = RequestContext(self.request, {})
        rendered_template = Template(template).render(context)
        self.assertEqual('<a href="%s">Home</a>' % url, rendered_template)

        # create a fake template without a name
        template = "{% load core_tags %}{% internal_link 'home' %}"

        # render the link
        context = RequestContext(self.request, {})
        rendered_template = Template(template).render(context)
        self.assertEqual('<a href="%s">%s</a>' % (url, url), rendered_template)

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

    def test_full_name(self):
        """ The full name is rendered correctly. """

        # create a fake template with a name
        template = "{% load core_tags %}{% full_name user %}"

        # render the tag
        context = Context({'user': self.user})
        rendered_template = Template(template).render(context)
        self.assertEqual(self.user.username, rendered_template)

        # add a first and a last name to the user
        self.user.first_name = 'Ulf'
        self.user.last_name = 'User'

        # render the tag
        context = Context({'user': self.user})
        rendered_template = Template(template).render(context)
        self.assertEqual('%s %s' % (self.user.first_name, self.user.last_name), rendered_template)
