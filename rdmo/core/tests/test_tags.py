from django.test import TestCase
from django.conf import settings

from django.template import RequestContext, Template
from django.test.client import RequestFactory
from django.utils import translation


class CoreTagsTests(TestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        super(CoreTagsTests, self).setUp()

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
