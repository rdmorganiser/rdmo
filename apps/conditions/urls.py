from django.conf.urls import url

from .views import ConditionsView, ConditionsExportView

urlpatterns = [
    url(r'^$', ConditionsView.as_view(), name='conditions'),
    url(r'^export/(?P<format>[a-z]+)/$', ConditionsExportView.as_view(), name='conditions_export'),
]
