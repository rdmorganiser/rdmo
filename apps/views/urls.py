from django.conf.urls import url

from .views import ViewsView, ViewsExportView

urlpatterns = [
    url(r'^$', ViewsView.as_view(), name='views'),
    url(r'^export/(?P<format>[a-z]+)/$', ViewsExportView.as_view(), name='views_export'),
]
