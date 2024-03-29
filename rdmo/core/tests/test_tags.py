from django.conf import settings
from django.template import RequestContext, Template
from django.urls import reverse
from django.utils import translation


def test_i18n_switcher(rf):
    """ The language switcher is rendered correctly. """

    # create a fake template with a name
    template = "{% load core_tags %}{% i18n_switcher %}"

    # set a language
    translation.activate(settings.LANGUAGES[0][0])

    # render the link
    request = rf.get(reverse('home'))
    context = RequestContext(request, {})
    rendered_template = Template(template).render(context)
    for language in settings.LANGUAGES:
        if language == settings.LANGUAGES[0]:
            assert '<a href="/i18n/{}/"><u>{}</u></a>'.format(*language) in rendered_template
        else:
            assert'<a href="/i18n/{}/">{}</a>'.format(*language) in rendered_template
