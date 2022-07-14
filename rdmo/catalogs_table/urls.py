from django.urls import re_path

from .views import CatalogsTableIndexView, CatalogsTableWrapperView, SitesListView, LockedListView
from .forms import CatalogsModalUpdateView, CatalogsLockedFormView, CatalogsSitesFormView


urlpatterns = [
    re_path(r'^$', CatalogsTableIndexView.as_view(), name='catalogs_table'),   
    re_path(r'table/', CatalogsTableWrapperView.as_view(), name='table_wrapper'),
    re_path(r'(?P<pk>[0-9]+)/update/modal', CatalogsModalUpdateView.as_view(), name='catalog_update_modal'),
    re_path(r'(?P<pk>[0-9]+)/update/locked', CatalogsLockedFormView.as_view(), name='column_update_locked'),
    re_path(r'(?P<pk>[0-9]+)/list/locked', LockedListView.as_view(), name='column_list_locked'),
    re_path(r'(?P<pk>[0-9]+)/update/sites', CatalogsSitesFormView.as_view(), name='column_update_sites'),
    re_path(r'(?P<pk>[0-9]+)/list/sites', SitesListView.as_view(), name='column_list_sites'),
]
