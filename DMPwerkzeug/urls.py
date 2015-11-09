from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from registration.backends.default.views import RegistrationView, ActivationView

from core import views

urlpatterns = [
    url(r'^$', 'core.views.home', name='home'),

    # login and logout
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),

    # change and retrieve password
    url(r'^password/change/$', auth_views.password_change, name='password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password-reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # user registration
    url(r'^register/$', RegistrationView.as_view(), name='registration_register'),
    url(r'^register/complete/$', TemplateView.as_view(template_name='registration/registration_complete.html'),
        name='registration_complete'),
    url(r'^activate/complete/$', TemplateView.as_view(template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$', ActivationView.as_view(), name='registration_activate'),
    url(r'^register/closed/$', TemplateView.as_view(template_name='registration/registration_closed.html'),
        name='registration_disallowed'),

    url(r'^admin/', include(admin.site.urls)),
]
