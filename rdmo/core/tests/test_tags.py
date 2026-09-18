from django.conf import settings
from django.template import RequestContext, Template
from django.urls import reverse


def test_i18n_switcher(rf):
    """ The language switcher is rendered correctly. """

    # create a fake template with a name
    template = "{% load core_tags %}{% i18n_switcher %}"

    # render the link
    request = rf.get(reverse('home'))
    context = RequestContext(request, {})
    rendered_template = Template(template).render(context)
    for language in settings.LANGUAGES:
        if language == settings.LANGUAGES[0]:
            assert 'href="/i18n/{}/"><u>{}</u>'.format(*language) in rendered_template
        else:
            assert 'href="/i18n/{}/">{}'.format(*language) in rendered_template
