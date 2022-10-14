from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from rdmo.core.views import ModelPermissionMixin
from rdmo.questions.models import Catalog

from  rdmo.catalogs_table.tables import CatalogsTable
from  rdmo.catalogs_table.viewsets import CatalogTableViewSet

from django_tables2 import SingleTableMixin

class CatalogsTableIndexView(ModelPermissionMixin, LoginRequiredMixin, SingleTableMixin, ListView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    table_class = CatalogsTable
    template_name = 'catalogs_table/table_index.html'
    
    def get_queryset(self):
        return CatalogTableViewSet.get_queryset(self)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class SitesListView(ModelPermissionMixin, LoginRequiredMixin, ListView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    template_name = 'catalogs_table/columns/sites.html'

    def get_queryset(self):
        return CatalogTableViewSet.get_queryset(self).get(pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        
        context_extra = {
                'sites': self.object_list.sites.values(),
                'all_sites' : Site.objects.count() == self.object_list.sites.values().count(),
                'pk' : str(self.kwargs['pk']),
                'sites_form_url' : reverse_lazy('column_sites_form', args=str(self.kwargs['pk'])),
                'sites_list_url' : reverse_lazy('column_sites_list', args=str(self.kwargs['pk'])),
                }
        
        context = {**context_data, **context_extra}
        return context
    