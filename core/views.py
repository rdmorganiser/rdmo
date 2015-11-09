from django.http import HttpResponseRedirect
from django.utils import translation


def i18n_switcher(request, language):
    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
