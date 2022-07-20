import pdb
import json

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import render
from django.template import loader

from rdmo.core.views import ModelPermissionMixin
from rdmo.core.constants import VALUE_TYPE_FILE
from rdmo.core.plugins import get_plugin
from rdmo.core.utils import markdown2html

from rdmo.questions.models import Catalog
# TODO add From Validators to prevent save when locked
# from rdmo.questions.validators import (CatalogLockedValidator, CatalogUniqueURIValidator)
'''
rdmo/rdmo/questions/admin.py
    def clean(self):
        CatalogUniqueURIValidator(self.instance)(self.cleaned_data)
        CatalogLockedValidator(self.instance)(self.cleaned_data)
'''
from rdmo.catalogs_table.utils import get_language_field_name

def htmx_httpresponse_headers(self, form, show_msg: str = None, redirect_url= None, **kwargs):
    ''' A response for a form that adds a HX-Trigger when the object was saved '''

    # print(f'HTMX httpresponse from: {self}')
    # print('Msg: ', show_msg)
    response = HttpResponse(
                
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "catalogChanged": True,
                        "showMessage": show_msg
                    }),

                    
                })
    if redirect_url:
        response.headers['HX-Redirect'] = redirect_url
    return response

class CatalogsModalUpdateView(ModelPermissionMixin, LoginRequiredMixin, UpdateView):
    ''' the form for the Modal inside catalogs_table '''
    permission_required = 'questions.view_catalog'
    model = Catalog
    fields = ('key', 'comment','locked','title_lang1', 'title_lang2', 'order', 'groups', 'sites')
    template_name = 'catalogs_table/partials/catalog_update_modal.html'
    success_url = reverse_lazy('catalogs_table')
    # TODO include validators to form
    # validators = ( CatalogUniqueURIValidator(), CatalogLockedValidator() )

    def form_valid(self, form):
        form.save()
        field_title = get_language_field_name('title')
        form_update_msg = f"Catalog {form.cleaned_data.get(field_title)} was updated"
        return htmx_httpresponse_headers(self, form, show_msg=form_update_msg)
       
            
class CatalogsLockedFormView(ModelPermissionMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    fields = ['locked']
    template_name = 'catalogs_table/columns/locked_form.html'
    success_url = reverse_lazy('table_list_locked')

    def form_valid(self, form):
        form.save()
        msg = f'{self.get_object().title} changed to {form.cleaned_data.get("locked")}'
        return htmx_httpresponse_headers(self, form, show_msg=msg)
       


class CatalogsSitesFormView(ModelPermissionMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    fields = ['sites']
    template_name = 'catalogs_table/columns/sites_form.html'

    def get_success_url(self) -> str:
        return reverse_lazy('column_list_sites', args=str(self.get_object().pk))

    def get_context_data(self, **kwargs):
        redirect_url = self.get_success_url()
        kwargs.update({'redirect_url' : redirect_url, 'pk' : str(self.get_object().pk)})
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        # TODO possibly add this message to response object
        form_update_msg = f"Catalog {self.get_object().title} was updated with: {', '.join(map(str, form.cleaned_data.get('sites')))}"

        sites_form_url = reverse_lazy('column_update_sites', args=str(self.get_object().pk))
        rendered = render(self.request, 'catalogs_table/columns/sites.html', 
                                        {'sites': form.cleaned_data['sites'].values(),
                                         'sites_form_url' : sites_form_url,
                                         'pk' : str(self.get_object().pk)
                                        })
        return rendered
