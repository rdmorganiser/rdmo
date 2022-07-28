import pdb
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

class CatalogsTableIndexView(ModelPermissionMixin, LoginRequiredMixin, TemplateView):
    permission_required = 'questions.view_catalog'
    template_name = 'catalogs_table/table_index.html'


class CatalogsTableWrapperView(ModelPermissionMixin, LoginRequiredMixin, SingleTableView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    table_class = CatalogsTable
    template_name = 'catalogs_table/table_wrapper.html'
    def get_queryset(self):
        return CatalogTableViewSet.get_queryset(self)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.headers.get('HX-Request', None) and 0:
            print(self)
            print(self.request.headers)
            print(self.request.path,'\n')
            # pdb.set_trace()
        return context
    def get_ordering(self):
        print('ordering called ', self)
        return super().get_ordering()


class SitesListView(ModelPermissionMixin, LoginRequiredMixin, ListView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    template_name = 'catalogs_table/columns/sites.html'

    def get_queryset(self):
        return CatalogTableViewSet.get_queryset(self).get(pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.object_list
        context['sites'] = self.object_list.sites.values()
        context['pk'] = str(self.kwargs['pk'])
        context['sites_form_url'] = reverse('column_sites_form', args=str(self.kwargs['pk'])) 
        return context
    
class LockedListView(ModelPermissionMixin, LoginRequiredMixin, ListView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    template_name = 'catalogs_table/columns/locked.html'

    def get_queryset(self):
        return CatalogTableViewSet.get_queryset(self).get(pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locked'] = self.object_list.locked
        context['locked_form_url'] = reverse('column_locked_form', args=str(self.kwargs['pk'])) 
        return context


class AvailableListView(ModelPermissionMixin, LoginRequiredMixin, ListView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    template_name = 'catalogs_table/columns/available.html'

    def get_queryset(self):
        return CatalogTableViewSet.get_queryset(self).get(pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available'] = self.object_list.available
        context['available_form_url'] = reverse('column_available_form', args=str(self.kwargs['pk'])) 
        return context