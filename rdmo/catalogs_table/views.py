from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, TemplateView, UpdateView, FormView

from rdmo.core.views import ModelPermissionMixin
from rdmo.questions.models import Catalog

from django_tables2 import SingleTableView, SingleTableMixin

from  rdmo.catalogs_table.tables import CatalogsTable
from  rdmo.catalogs_table.forms import CatalogsTableForm, CatalogsLockedForm
from  rdmo.catalogs_table.viewsets import CatalogTableViewSet

class CatalogsTableIndexView(ModelPermissionMixin, LoginRequiredMixin, SingleTableMixin, FormView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    table_class = CatalogsTable
    form_class = CatalogsTableForm
    # table_data = CatalogTableViewSet.get_queryset()
    template_name = 'catalogs_table/table_index.html'
    
    def get_queryset(self):
        return CatalogTableViewSet.get_queryset(self)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self, request, *args, **kwarg):
        
        post_keys = request.POST.keys()
        _form_class = None
        if 'locked' in post_keys:
            _form_class = CatalogsLockedForm
        # breakpoint()
        form = self.get_form(form_class=_form_class)
        if form.is_valid():
            return form.form_valid(form)
        else:
            return self.form_invalid(form)
        
        
    

class SitesListView(ModelPermissionMixin, LoginRequiredMixin, ListView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    template_name = 'catalogs_table/columns/sites.html'

    def get_queryset(self):
        return CatalogTableViewSet.get_queryset(self).get(pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breakpoint()
        context['sites'] = self.object_list.sites.values()
        # sites|length  == Site.objects.count() or sites|length == 0
        
        context['all_sites'] = Site.objects.count() == context['sites'].count()
        context['pk'] = str(self.kwargs['pk'])
        context['sites_form_url'] = reverse('column_sites_form', args=str(self.kwargs['pk'])) 
        return context
    