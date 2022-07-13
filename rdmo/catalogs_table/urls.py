from django.urls import re_path, path

from .views import CatalogsTableBodyView,CatalogsTableWrapperView, CatalogsTableIndexView, SitesListView, LockedListView
# 
from .forms import CatalogsModalUpdateView, CatalogsLockedFormView, CatalogsSitesFormView


urlpatterns = [
    re_path(r'^$', CatalogsTableIndexView.as_view(), name='catalogs_table'),   
    path(r'table/', CatalogsTableWrapperView.as_view(), name='table_wrapper'),
    path(r'update/<int:pk>/', CatalogsModalUpdateView.as_view(), name='table_update_catalog_modal'),
    # path(r'table', CatalogsModalFormView.as_view(), name='catalogs_table_table'),
    path(r'update/<int:pk>/locked', CatalogsLockedFormView.as_view(), name='table_update_locked'),
    path(r'list/<int:pk>/locked', LockedListView.as_view(), name='table_list_locked'),
    path(r'update/<int:pk>/sites', CatalogsSitesFormView.as_view(), name='table_update_sites'),
    path(r'list/<int:pk>/sites', SitesListView.as_view(), name='table_list_sites'),
]
