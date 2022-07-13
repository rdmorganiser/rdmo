import pdb
import json
import re
from django.db import models
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, FormView, ListView, TemplateView
from django.views.generic.edit import FormMixin

from rdmo.core.views import ModelPermissionMixin
from rdmo.questions.models import Catalog

from django_tables2 import SingleTableView

from rdmo.catalogs_table.forms import CatalogTableForm
from  rdmo.catalogs_table.tables import CatalogsTable
from  rdmo.catalogs_table.viewsets import CatalogTableViewSet

class CatalogsTableBodyView(ModelPermissionMixin, LoginRequiredMixin, SingleTableView):
        permission_required = 'questions.view_catalog'
        model = Catalog
        table_class = CatalogsTable
        # table_data = CatalogTableViewSet
        template_name = 'catalogs_table/table_body.html'
        # form_class = CatalogTableForm
        
        def get_queryset(self):
            print(f' get_qset: {self}')
            # pdb.set_trace()
            return CatalogsTableIndexView.get_queryset(self)
        
        def get_ordering(self):
            """Return the field or fields to use for ordering the queryset."""
            print(f'{self} get_ordering, {self.ordering}')
            
            return self.ordering

        def dispatch(self, request, *args, **kwargs):
            # dispatch = super().dispatch(request, *args, **kwargs)
            
            # request = check_sprinkles(request)
            # pdb.set_trace()
            # if 'sort' in self.kwargs.keys():
            if 'hx-request' in request.headers:
                request.META['HX-Trigger'] = json.dumps({
                        "catalogChanged": None,
                        "showMessage": f"CATALOGS added."})

            # print(f'dispatch {self} ', request.headers)
            return super().dispatch(request, *args, **kwargs)
            
            
            # return request

        
        def _options(self, request, *args, **kwargs):
            """Handle responding to requests for the OPTIONS HTTP verb."""
            response = HttpResponse()
            response.headers['Allow'] = ', '.join(self._allowed_methods())
            response.headers['Content-Length'] = '0'
            
            _dct = {'HX-Trigger': json.dumps({
                        "catalogChanged": None,
                        "showMessage": f"CATALOGS added."})
            }
            return response

class CatalogsTableIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'catalogs_table/catalogs_table_index.html'


class CatalogsTableWrapperView(ModelPermissionMixin, LoginRequiredMixin, SingleTableView):
    # FormMixin
    permission_required = 'questions.view_catalog'
    model = Catalog
    table_class = CatalogsTable
    # table_data = CatalogTableViewSet # set with get_queryset()
    template_name = 'catalogs_table/table_wrapper.html'
    # template_name = 'catalogs_table/catalogs_table_index.html'
    # form_class = CatalogTableForm
    # success_url = reverse_lazy('catalogs_table')
    
    # success_url = '/thanks/'
    def get_queryset(self):
        return CatalogTableViewSet.get_queryset(self)
        #  return super().get_queryset()
    # def dispatch(self, request, *args, **kwargs):
    #     print('dispatch {self}')
    # # Try to dispatch to the right method; if a method doesn't exist,
    # # defer to the error handler. Also defer to the error handler if the
    # # request method isn't on the approved list.
    #     if request.method.lower() in self.http_method_names:
    #         handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
    #     else:
    #         handler = self.http_method_not_allowed
    #     return handler(request, *args, **kwargs)
    
class SitesListView(ListView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    template_name = 'catalogs_table/columns/sites.html'

    def get_queryset(self):
        return CatalogTableViewSet.get_queryset(self).get(pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pdb.set_trace()
        self.object_list
        context['sites'] = self.object_list.sites.values()
        _pk = str(self.kwargs['pk'])
        context['pk'] = _pk
        context['sites_form_url'] = reverse('table_update_sites', args=str(self.kwargs['pk'])) 
        # Voucher.objects.filter(name__icontains='greenfeld')
        # context['roys'] =
        # Voucher.objects.filter(name__icontains='roy')
        return context
    
   
    def render_template_from_context(self, request, sites=None, sites_form_url=None, pk=None):
        rendered = render(request, self.template_name, 
                                        {
                                        'sites': sites,
                                        'sites_form_url' : sites_form_url,
                                        'pk' : pk
                                         }
                                         )
        return rendered




class LockedListView(ListView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    template_name = 'catalogs_table/columns/locked.html'

    def get_queryset(self):
        return CatalogTableViewSet.get_queryset(self).get(pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pdb.set_trace()
        self.object_list
        context['locked'] = self.object_list.locked.values()
        context['update_locked_url'] = reverse('table_update_locked', args=str(self.kwargs['pk'])) 
        # Voucher.objects.filter(name__icontains='greenfeld')
        # context['roys'] =
        # Voucher.objects.filter(name__icontains='roy')
        return context


def movie_list(request):
    return render(request, 'movie_list.html', {
        'movies': Movie.objects.all(),
    })
