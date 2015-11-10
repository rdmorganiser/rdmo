from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation
from django.core.urlresolvers import reverse, resolve, Resolver404
from django.utils.six.moves.urllib.parse import urlparse
from django.conf import settings


def not_found(request):
    current_language = translation.get_language()
    path = request.path
    if settings.APPEND_SLASH and not path.endswith('/'):
        path += '/'

    for language, language_string in settings.LANGUAGES:
        if language != current_language:
            # activate the new language for now
            translation.activate(language)
            try:
                # get the name for the for the new language
                name = resolve(path).url_name

                # set the new language in the session
                request.session[translation.LANGUAGE_SESSION_KEY] = language

                # get the url for the new language and redirect
                new_url = reverse(name)
                return HttpResponseRedirect(new_url)
            except Resolver404:
                pass

    # activate the current language again
    translation.activate(current_language)

    # render the 404 template
    return render(request, 'core/404.html', status=404)


def i18n_switcher(request, language):
    # get the name for the refering url
    next = request.META.get('HTTP_REFERER', None) or '/'
    name = resolve(urlparse(next)[2]).url_name

    # set the new language
    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language

    # get the url for the new language and redirect
    new_url = reverse(name)
    return HttpResponseRedirect(new_url)
