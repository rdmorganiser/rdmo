from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import *

urlpatterns = [
    url(r'^$', domain, name='domain'),

    url(_(r'^attributes/create$'), AttributeCreateView.as_view(), name='attribute_create'),
    url(_(r'^attributes/(?P<pk>[0-9]+)/update$'), AttributeUpdateView.as_view(), name='attribute_update'),
    url(_(r'^attributes/(?P<pk>[0-9]+)/delete$'), AttributeDeleteView.as_view(), name='attribute_delete'),

    url(_(r'^attributesets/create$'), AttributeSetCreateView.as_view(), name='attributeset_create'),
    url(_(r'^attributesets/(?P<pk>[0-9]+)/update$'), AttributeSetUpdateView.as_view(), name='attributeset_update'),
    url(_(r'^attributesets/(?P<pk>[0-9]+)/delete$'), AttributeSetDeleteView.as_view(), name='attributeset_delete'),
]
