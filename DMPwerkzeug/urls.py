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
    url(r'^password-reset/$', auth_views.password_reset, {'template_name': 'auth/password_reset.html', 'email_template_name': 'auth/password_reset_email.html', 'subject_template_name': 'auth/password_reset_subject.txt'}, name='password_reset'),
    url(r'^password-reset/done/$', auth_views.password_reset_done, {'template_name': 'auth/password_reset_done.html'}, name='password_reset_done'),
    url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'template_name': 'auth/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', auth_views.password_reset_complete, {'template_name': 'auth/password_reset_complete.html'}, name='password_reset_complete'),

    url(r'^admin/', include(admin.site.urls)),
]
