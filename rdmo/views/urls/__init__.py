from django.urls import include, re_path

from rest_framework import routers

from ..views import ViewsExportView, ViewsImportXMLView, ViewsView

urlpatterns = [
    re_path(r'^$', ViewsView.as_view(), name='views'),
    re_path(r'^export/(?P<format>[a-z]+)/$', ViewsExportView.as_view(), name='views_export'),
    re_path(r'^import/(?P<format>[a-z]+)/$', ViewsImportXMLView.as_view(), name='views_import'),
]
