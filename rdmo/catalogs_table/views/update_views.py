import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.utils.translation import gettext
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import render

from rdmo.core.views import ModelPermissionMixin
from rdmo.questions.models import Catalog


class HTMXResponse(HttpResponse):
    ''' adds the HTMX headers to a HttpRepsonse '''

    def __init__(self,
                    status=204,
                    trigger_name=None,
                    trigger_val=None,
                    message=None,
                    redirect=None,
                    refresh=None,
                    location=None
                    ):
        super().__init__(status=status)
        hx_trigger = {}
        if trigger_name:
            hx_trigger.update({trigger_name: trigger_val})
        if message:
            hx_trigger.update({"showMessage": message})
        
        if hx_trigger:
            self.headers['HX-Trigger'] = json.dumps(hx_trigger)
        if redirect:
            self.headers['HX-Redirect'] = json.dumps(redirect)
        if refresh:
            self.headers['HX-Refresh'] = "true"
        if location:
            self.headers['HX-Location'] = json.dumps(location)


class CatalogsLockedUpdateView(ModelPermissionMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    fields = ('locked',)
    template_name = 'catalogs_table/columns/locked_form.html'

    def form_valid(self, form):
        
        form.save()
        htmx_kwargs = {
            'message' : f'{self.get_object().title} changed to {form.cleaned_data.get("locked")}',
            'trigger_name' : f'lockedChanged-{self.get_object().pk}'
        }
        return HTMXResponse(**htmx_kwargs)

class CatalogsAvailableUpdateView(ModelPermissionMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    fields = ('available',)
    template_name = 'catalogs_table/columns/available_form.html'
    
    def form_valid(self, form):
        if form.has_changed() and self.object.locked:
            pass # Perhaps raise a validation error here
        form.save()
        htmx_kwargs = {
            'message' : f'{self.get_object().title} changed to {form.cleaned_data.get("available")}',
            'trigger_name' : f'availableChanged-{self.get_object().pk}'
        }
        return HTMXResponse(**htmx_kwargs)


class CatalogsSitesUpdateView(ModelPermissionMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    fields = ('sites',)
    template_name = 'catalogs_table/columns/sites_form.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
                       'pk' : str(self.get_object().pk)
                    })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        
        form.save()
        htmx_kwargs = {
            'message' : gettext("Sites updated"),
            'trigger_name' : f'sitesChanged-{self.get_object().pk}'
        }
        return HTMXResponse(**htmx_kwargs)
        