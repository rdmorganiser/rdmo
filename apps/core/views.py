from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from allauth.account.forms import LoginForm

from .utils import get_script_alias, get_referer_path_info, get_next, get_referer


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('projects'))
    else:
        return render(request, 'core/home.html', {'form': LoginForm()})


def i18n_switcher(request, language):
    next = get_referer_path_info(request, default='/')
    resolver_match = resolve(next)

    # get extra stuff in the url to carry over to the new url (for angular)
    old_url = reverse(resolver_match.url_name, kwargs=resolver_match.kwargs)
    extra = next.replace(old_url.replace(get_script_alias(request), ''), '')

    # set the new language
    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language

    # get the url for the new language and redirect
    new_url = reverse(resolver_match.url_name, kwargs=resolver_match.kwargs)
    return HttpResponseRedirect(new_url + extra)


class RedirectViewMixin(View):

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            next = get_next(request)
            return HttpResponseRedirect(next)
        else:
            return super(RedirectViewMixin, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(RedirectViewMixin, self).get_context_data(**kwargs)
        if 'next' in self.request.GET:
            context_data['next'] = self.request.GET['next']
        else:
            context_data['next'] = get_referer(self.request)
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
