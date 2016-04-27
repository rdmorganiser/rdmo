from django.conf.urls import url, include
from django.utils.translation import ugettext_lazy as _

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, base_name='project')
router.register(r'entities', ValueEntityViewSet, base_name='entity')
router.register(r'values', ValueViewSet, base_name='value')
router.register(r'valuesets', ValueSetViewSet, base_name='valuesets')

urlpatterns = [
    url(r'^$', projects, name='projects'),
    url(r'^(?P<pk>[0-9]+)/$', project, name='project'),
    url(_(r'^create$'), ProjectCreateView.as_view(), name='project_create'),
    url(_(r'^(?P<pk>[0-9]+)/update/$'), ProjectUpdateView.as_view(), name='project_update'),
    url(_(r'^(?P<pk>[0-9]+)/delete/$'), ProjectDeleteView.as_view(), name='project_delete'),

    url(r'^(?P<project_id>[0-9]+)/questions/', project_questions, name='project_questions'),

    url(r'^api/', include(router.urls)),
]
