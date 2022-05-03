from django.urls import re_path

from .views import CatalogsTableView

urlpatterns = [
    re_path(r'^$', CatalogsTableView.as_view(), name='catalogs_table'),   
]
