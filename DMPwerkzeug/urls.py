from django.conf.urls import include, url
from django.contrib import admin

from core import views

urlpatterns = [
    url(r'^$', 'core.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
]
