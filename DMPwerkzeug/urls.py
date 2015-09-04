from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from core import views

urlpatterns = [
    url(r'^$', 'core.views.home', name='home'),

    url(r'^login/$', auth_views.login, {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
    url(r'^password-change/$', auth_views.password_change, {'template_name': 'auth/password_change.html'}, name='password_change'),
    url(r'^password-change/done/$', auth_views.password_change_done, {'template_name': 'auth/password_change_done.html'}, name='password_change_done'),

    # url(r'^login$', 'access.views.login', name='login'),
    # url(r'^logout$', 'access.views.logout', name='logout'),

    url(r'^admin/', include(admin.site.urls)),
]
