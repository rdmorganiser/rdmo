from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import interview, interview_create, interview_update, interview_delete

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)$', interview, name='interview'),
    url(r'^%s$' % _('create'), interview_create, name='interview_create'),
    url(r'^(?P<pk>[0-9]+)/%s$' % _('update'), interview_update, name='interview_update'),
    url(r'^(?P<pk>[0-9]+)/%s$' % _('delete'), interview_delete, name='interview_delete'),
]
