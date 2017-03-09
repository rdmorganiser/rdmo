from django.conf.urls import url

from .views import OptionsView, OptionsExportView

urlpatterns = [
    url(r'^$', OptionsView.as_view(), name='options'),
    url(r'^export/(?P<format>[a-z]+)/$', OptionsExportView.as_view(), name='options_export'),
]
