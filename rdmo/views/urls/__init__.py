from django.urls import re_path

from ..views import ViewsExportView, ViewsView

urlpatterns = [
    re_path(r'^$', ViewsView.as_view(), name='views'),
    re_path(r'^export/(?P<format>[a-z]+)/$', ViewsExportView.as_view(), name='views_export'),
]
