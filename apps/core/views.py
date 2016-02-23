from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, resolve, Resolver404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView



from .utils import get_referer_path_info


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('projects'))
    else:
        return render(request, 'core/home.html')


def not_found(request):
    current_language = translation.get_language()
    path = request.path_info
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
    next = get_referer_path_info(request, default='/')
    name = resolve(next).url_name

    # set the new language
    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language

    # get the url for the new language and redirect
    new_url = reverse(name)
    return HttpResponseRedirect(new_url)


class RedirectViewMixin(View):

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            if 'next' in request.POST:
                url = request.POST['next']
            else:
                try:
                    url = self.get_object().get_absolute_url()
                except AttributeError:
                    url = '/'

            return HttpResponseRedirect(url)
        else:
            return super(RedirectViewMixin, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(RedirectViewMixin, self).get_context_data(**kwargs)
        if 'next' in self.request.GET:
            context_data['next'] = self.request.GET['next']
        elif 'HTTP_REFERER' in self.request.META:
            context_data['next'] = self.request.META['HTTP_REFERER']
        return context_data

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']
        else:
            return super(RedirectViewMixin, self).get_success_url()


class ProtectedCreateView(RedirectViewMixin, CreateView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedCreateView, self).dispatch(*args, **kwargs)


class ProtectedUpdateView(RedirectViewMixin, UpdateView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedUpdateView, self).dispatch(*args, **kwargs)


class ProtectedDeleteView(RedirectViewMixin, DeleteView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedDeleteView, self).dispatch(*args, **kwargs)
