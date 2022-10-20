from django.urls import re_path, path

from .views.views import CatalogsTableIndexView, CatalogsTableWrapperView, SitesListView
from .views.update_views import CatalogsLockedUpdateView, CatalogsAvailableUpdateView, CatalogsSitesUpdateView

# app_name = 'catalogs_table'

urlpatterns = [
    re_path(r'^$', CatalogsTableIndexView.as_view(), name='catalogs_table'),   
    re_path('table', CatalogsTableWrapperView.as_view(), name='table_wrapper'),   
    path('<int:pk>/sites/list/', SitesListView.as_view(), name='column_sites_list'),
    path('<int:pk>/sites/update/', CatalogsSitesUpdateView.as_view(), name='column_sites_form'),
    path('<int:pk>/locked/update/', CatalogsLockedUpdateView.as_view(), name='column_locked_form'),
    path('<int:pk>/available/update/', CatalogsAvailableUpdateView.as_view(), name='column_available_form'),
    
]