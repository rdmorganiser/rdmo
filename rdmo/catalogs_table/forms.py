import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import render
from django.template.loader import render_to_string

from rdmo.core.views import ModelPermissionMixin
from rdmo.questions.models import Catalog

# TODO add From Validators to prevent save when locked
# from rdmo.questions.validators import (CatalogLockedValidator, CatalogUniqueURIValidator)
'''
rdmo/rdmo/questions/admin.py
    def clean(self):
        CatalogUniqueURIValidator(self.instance)(self.cleaned_data)
        CatalogLockedValidator(self.instance)(self.cleaned_data)
'''
from rdmo.catalogs_table.utils import get_language_field_name, parse_sort_query


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
            if 0:
                print(f'HTMX httpresponse from: {self}')
                print(f'Name: {trigger_name}, Msg: {message}')
        if redirect:
            self.headers['HX-Redirect'] = json.dumps(redirect)
        if refresh:
            self.headers['HX-Refresh'] = "true"
        if location:
            self.headers['HX-Location'] = json.dumps(location)

        # pdb.set_trace()

class CatalogsModalUpdateView(ModelPermissionMixin, LoginRequiredMixin, UpdateView):
    ''' the form for the Modal inside catalogs_table '''
    permission_required = 'questions.view_catalog'
    model = Catalog
    fields = ('key', 'comment','locked','available', 'title_lang1', 'title_lang2', 'order', 'groups', 'sites')
    template_name = 'catalogs_table/columns/update_form.html'
    success_url = reverse_lazy('table_wrapper')
    # TODO include validators to form
    # validators = ( CatalogUniqueURIValidator(), CatalogLockedValidator() )
    def get(self, request, *args, **kwargs):
         
        get = super().get(request, *args, **kwargs)
        
        # if url_ref_query(url_ref):
        context = self.get_context_data(**kwargs)

        # TODO: pass this sort query from referer to table wrapper after POST
        # TODO: so that the same sorting is maintained after submitting the modal form
        url_ref = request.META.get('HTTP_REFERER')
        context['updatemodal_REF_QUERY'] = parse_sort_query(url_ref)
        if 0:
            print('\n', self)
            print(context, '\n')
            # pdb.set_trace()       
        return self.render_to_response(context)

    def form_valid(self, form):
        form.save()
        field_title = get_language_field_name('title')
        context = self.get_context_data()
        if 0:
            print('\n', self)
            print(context, '\n')
            print(self.request.headers, '\n')
            # pk =  str(self.get_object().pk)
            # trigger = f'lockedChanged-{pk}'
        trigger = 'catalogUpdated'
        
        redirect = self.success_url+parse_sort_query(self.request.headers['Referer'])
        form_update_msg = f"Catalog {form.cleaned_data.get(field_title)} was updated, {context.get('updatemodal_REF_QUERY')}"
        htmx_response = HTMXResponse(trigger_name=trigger,
                                     message=form_update_msg,
                                     redirect=None,
                                     refresh=False,
                                     location={"target":"#container-table-index"})
        
        return htmx_response
       
            
class CatalogsLockedFormView(ModelPermissionMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    fields = ['locked']
    template_name = 'catalogs_table/columns/locked_form.html'
    success_url = reverse_lazy('column_locked_list')

    def form_valid(self, form):
        form.save()
        msg = f'{self.get_object().title} changed to {form.cleaned_data.get("locked")}'
        pk =  str(self.get_object().pk)
        trigger = f'lockedChanged-{pk}'
        return HTMXResponse(trigger_name=trigger, message=msg)

class CatalogsAvailableFormView(ModelPermissionMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    fields = ['available']
    template_name = 'catalogs_table/columns/available_form.html'
    success_url = reverse_lazy('column_available_list')

    def form_valid(self, form):
        # super().form_valid(form)
        form.save()
        msg = f'{self.get_object().title} changed to {form.cleaned_data.get("available")}'
        pk =  str(self.get_object().pk)
        trigger = f'availableChanged-{pk}'
        return HTMXResponse(trigger_name=trigger, message=msg)
        # return htmx_httpresponse_headers(self, form, trigger_name= trigger, show_msg=msg)


class CatalogsSitesFormView(ModelPermissionMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    fields = ['sites']
    template_name = 'catalogs_table/columns/sites_form.html'

    def get_success_url(self) -> str:
        return reverse_lazy('column_sites_list', args=str(self.get_object().pk))

    def get_context_data(self, **kwargs):
        redirect_url = self.get_success_url()
        kwargs.update({'redirect_url' : redirect_url, 'pk' : str(self.get_object().pk)})
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        # TODO possibly add this message to response object
        form_update_msg = f"Catalog {self.get_object().title} was updated with: {', '.join(map(str, form.cleaned_data.get('sites')))}"

        sites_form_url = reverse_lazy('column_sites_form', args=str(self.get_object().pk))
        context = {
                'sites': form.cleaned_data['sites'].values(),
                'len_all_sites' : len(Site.objects.all()),
                'sites_form_url' : sites_form_url,
                'pk' : str(self.get_object().pk)
                }
        rendered = render_column_sites(request=self.request, context=context)
        
        return rendered


def render_column_sites(request= None, template_name = 'catalogs_table/columns/sites.html', context=None):
        if request:
            rendered = render(request, template_name, context)
        else:
            rendered = render_to_string(template_name, context)
        return rendered
