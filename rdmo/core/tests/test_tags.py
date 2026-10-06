import pytest

from django.conf import settings
from django.template import RequestContext, Template
from django.urls import reverse
from django.utils import translation


@pytest.mark.parametrize('active_language', [code for code, _ in settings.LANGUAGES])
def test_i18n_switcher(rf, active_language):
    """ The language switcher is rendered correctly. """

    # create a fake template with a name
    template = "{% load core_tags %}{% i18n_switcher %}"

    # render the link
    request = rf.get(reverse('home'))
    context = RequestContext(request, {})
    with translation.override(active_language):
        rendered_template = Template(template).render(context)
        for code, label in settings.LANGUAGES:
            url = reverse('i18n_switcher', args=[code])
            text = f'<u>{label}</u>' if code == active_language else str(label)

            assert f'<a href="{url}">{text}</a>' in rendered_template
