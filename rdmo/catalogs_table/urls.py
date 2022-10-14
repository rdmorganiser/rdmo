from django.urls import re_path

from rdmo.catalogs_table.views.views import CatalogsTableIndexView, SitesListView
from rdmo.catalogs_table.views.update_views import CatalogsLockedFormView, CatalogsAvailableFormView, CatalogsSitesFormView

urlpatterns = [
    re_path(r'^$', CatalogsTableIndexView.as_view(), name='catalogs_table'),   
    re_path(r'(?P<pk>[0-9]+)/update/locked', CatalogsLockedFormView.as_view(), name='column_locked_form'),
    re_path(r'(?P<pk>[0-9]+)/update/available', CatalogsAvailableFormView.as_view(), name='column_available_form'),
    re_path(r'(?P<pk>[0-9]+)/update/sites', CatalogsSitesFormView.as_view(), name='column_sites_form'),
    re_path(r'(?P<pk>[0-9]+)/list/sites', SitesListView.as_view(), name='column_sites_list'),
]