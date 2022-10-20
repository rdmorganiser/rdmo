from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.views.generic import ListView, TemplateView

from rdmo.core.views import ModelPermissionMixin
from rdmo.questions.models import Catalog

from ..tables import CatalogsTable
from ..filters import CatalogsFilter

from django_filters.views import FilterView
from django_tables2 import SingleTableMixin


class CatalogsTableIndexView(ModelPermissionMixin, LoginRequiredMixin, FilterView):
    permission_required = 'questions.view_catalog'
    template_name = 'catalogs_table/table_index.html'
    filterset_class = CatalogsFilter


class CatalogsTableWrapperView(ModelPermissionMixin, LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    table_class = CatalogsTable
    template_name = 'catalogs_table/table_wrapper.html'
    filterset_class = CatalogsFilter
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class SitesListView(ModelPermissionMixin, LoginRequiredMixin, ListView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    template_name = 'catalogs_table/columns/sites_list.html'

    def get_queryset(self):
        return Catalog.objects.get(pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        
        context_extra = {
                'sites': self.object_list.sites.values(),
                'has_all_sites' : Site.objects.count() == self.object_list.sites.values().count(),
                'pk' : str(self.kwargs['pk']),
                }
        
        context = {**context_data, **context_extra}
        return context
    