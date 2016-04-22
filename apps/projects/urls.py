from django.conf.urls import url, include
from django.utils.translation import ugettext_lazy as _

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, base_name='project')
router.register(r'values', ValueViewSet, base_name='value')
router.register(r'valuesets', ValueSetViewSet, base_name='valuesets')

urlpatterns = [
    url(r'^$', projects, name='projects'),
    url(r'^(?P<pk>[0-9]+)/$', project, name='project'),
    url(_(r'^create$'), ProjectCreateView.as_view(), name='project_create'),
    url(_(r'^(?P<pk>[0-9]+)/update/$'), ProjectUpdateView.as_view(), name='project_update'),
    url(_(r'^(?P<pk>[0-9]+)/delete/$'), ProjectDeleteView.as_view(), name='project_delete'),

    url(r'^(?P<project_id>[0-9]+)/questions/$', project_questions, name='project_questions'),
    url(r'^(?P<project_id>[0-9]+)/questions/(?P<entity_id>[0-9]+)/$', project_questions, name='project_questions'),

    #url(r'^(?P<project_id>[0-9]+)/questions/$', project_questions_form, name='project_questions_form'),
    # url(r'^(?P<project_id>[0-9]+)/questions/(?P<question_entity_id>[0-9]+)/$', project_questions_form, name='project_questions_form'),
    # url(r'^(?P<project_id>[0-9]+)/questions/(?P<question_entity_id>[0-9]+)/prev/$', project_questions_prev, name='project_questions_prev'),
    # url(r'^(?P<project_id>[0-9]+)/questions/(?P<question_entity_id>[0-9]+)/next/$', project_questions_next, name='project_questions_next'),

    url(r'^api/', include(router.urls)),
]
