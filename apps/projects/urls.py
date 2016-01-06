from django.conf.urls import url

from .views import projects, project

urlpatterns = [
    # edit own profile
    url(r'^$', projects, name='projects'),
    url(r'^(?P<pk>[0-9]+)$', project, name='project'),
]
