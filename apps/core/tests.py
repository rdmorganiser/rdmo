from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.template import RequestContext, Template
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import Site
from django.utils import translation


class TestListViewMixin():

    def test_list_view(self):
        url = reverse(self.list_url_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestRetrieveViewMixin():

    def test_retrieve_view(self):
        url = reverse(self.retrieve_url_name, args=[self.object.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestCreateViewMixin():

    def test_create_view_get(self):
        url = reverse(self.create_url_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_post(self):
        url = reverse(self.create_url_name)

        model_dict = model_to_dict(self.object)
        data = {}
        for key in model_dict:
            if model_dict[key] is not None:
                data[key] = model_dict[key]

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class TestUpdateViewMixin():

    def test_update_view_get(self):
        url = reverse(self.update_url_name, args=[self.object.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_post(self):
        url = reverse(self.update_url_name, args=[self.object.pk])

        model_dict = model_to_dict(self.object)
        data = {}
        for key in model_dict:
            if model_dict[key] is not None:
                data[key] = model_dict[key]

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class TestDeleteViewMixin():

    def test_delete_get(self):
        url = reverse(self.delete_url_name, args=[self.object.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        url = reverse(self.delete_url_name, args=[self.object.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)


class TestModelStringMixin():

    def test_model_str(self):
        self.assertIsNotNone(self.object.__str__())


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
        self.assertRedirects(response, reverse('projects'))

        # test as superuser
        client.login(username='admin', password='password')
        response = client.get('/')
        self.assertRedirects(response, reverse('projects'))

    def test_not_found(self):
        ''' The redirect when accessing a link in a non active language works. '''

        # get the client object
        client = Client()

        # get the login link in german
        translation.activate('de')
        url = reverse('registration_register')

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
        template = "{% load core_tags %}{% internal_link 'Home' 'home' %}"

        # render the link
        context = RequestContext(self.request, {})
        rendered_template = Template(template).render(context)
        self.assertEqual('<a href="%s">Home</a>' % url, rendered_template)

        # create a fake template without a name
        template = "{% load core_tags %}{% internal_link None 'home' %}"

        # render the link
        context = RequestContext(self.request, {})
        rendered_template = Template(template).render(context)
        self.assertEqual('<a href="%s">%s</a>' % (url, url), rendered_template)

        # create a fake template with a permission
        template = "{% load core_tags %}{% internal_link 'Home' 'home' permission='permission' %}"

        # render the link
        context = RequestContext(self.request, {})
        self.request.user = AnonymousUser()
        rendered_template = Template(template).render(context)
        self.assertEqual('', rendered_template)

        # create a fake template with the login_required permission
        template = "{% load core_tags %}{% internal_link 'Home' 'home' permission='login_required' %}"

        # render the link with the anonymous user
        context = RequestContext(self.request, {})
        self.request.user = AnonymousUser()
        rendered_template = Template(template).render(context)
        self.assertEqual('', rendered_template)

        # render the link with a proper user
        context = RequestContext(self.request, {})
        self.request.user = self.user
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
