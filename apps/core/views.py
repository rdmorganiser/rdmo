from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from allauth.account.forms import LoginForm

from .utils import get_referer, get_referer_path_info, get_next


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('projects'))
    else:
        return render(request, 'core/home.html', {'form': LoginForm()})


def i18n_switcher(request, language):
    referer = get_referer(request, default='/')

    # set the new language
    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language

    return HttpResponseRedirect(referer)


class RedirectViewMixin(View):

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return HttpResponseRedirect(get_next(request))
        else:
            return super(RedirectViewMixin, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(RedirectViewMixin, self).get_context_data(**kwargs)
        if 'next' in self.request.GET:
            context_data['next'] = self.request.GET['next']
        else:
            context_data['next'] = get_referer_path_info(self.request)
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
