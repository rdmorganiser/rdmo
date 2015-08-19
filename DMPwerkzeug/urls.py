from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from core import views

urlpatterns = [
    url(r'^$', 'core.views.home', name='home'),

    url(r'^login/$', auth_views.login, {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),

    # url(r'^login$', 'access.views.login', name='login'),
    # url(r'^logout$', 'access.views.logout', name='logout'),

    url(r'^admin/', include(admin.site.urls)),
]
