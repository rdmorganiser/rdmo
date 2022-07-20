import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, TemplateView

from rdmo.core.views import ModelPermissionMixin
from rdmo.questions.models import Catalog

from django_tables2 import SingleTableView

from  rdmo.catalogs_table.tables import CatalogsTable
from  rdmo.catalogs_table.viewsets import CatalogTableViewSet

class CatalogsTableIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'catalogs_table/catalogs_table_index.html'


class CatalogsTableWrapperView(ModelPermissionMixin, LoginRequiredMixin, SingleTableView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    table_class = CatalogsTable
    template_name = 'catalogs_table/table_wrapper.html'
    def get_queryset(self):
        return CatalogTableViewSet.get_queryset(self)
    
class SitesListView(ModelPermissionMixin, LoginRequiredMixin, ListView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    template_name = 'catalogs_table/columns/sites.html'

    def get_queryset(self):
        return CatalogTableViewSet.get_queryset(self).get(pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object_list
        context['sites'] = self.object_list.sites.values()
        pk = str(self.kwargs['pk'])
        context['pk'] = pk
        context['sites_form_url'] = reverse('column_update_sites', args=pk) 
        return context
    
   
    def _render_template_from_context(self, request, sites=None, sites_form_url=None, pk=None):
        rendered = render(request, self.template_name, 
                                        {
                                        'sites': sites,
                                        'sites_form_url' : sites_form_url,
                                        'pk' : pk
                                         }
                         )
        return rendered


class LockedListView(ModelPermissionMixin, LoginRequiredMixin, ListView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    template_name = 'catalogs_table/columns/locked.html'

    def get_queryset(self):
        return CatalogTableViewSet.get_queryset(self).get(pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object_list
        context['locked'] = self.object_list.locked.values()
        context['update_locked_url'] = reverse('column_update_locked', args=str(self.kwargs['pk'])) 
        return context
