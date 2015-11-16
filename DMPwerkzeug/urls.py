from django.conf.urls import include, url
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from registration.backends.default.views import RegistrationView, ActivationView

handler404 = 'core.views.not_found'

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='core/home.html'), name='home'),

    # edit own profile
    url(_(r'^profile/$'), 'accounts.views.profile', name='profile_update'),

    # login and logout
    url(_(r'^login/$'), auth_views.login, name='login'),
    url(_(r'^logout/$'), auth_views.logout, {'next_page': 'home'}, name='logout'),

    # change and retrieve password
    url(_(r'^password/change/$'), auth_views.password_change, name='password_change'),
    url(_(r'^password/change/done/$'), auth_views.password_change_done, name='password_change_done'),
    url(_(r'^password/reset/$'), auth_views.password_reset, name='password_reset'),
    url(_(r'^password/reset/done/$'), auth_views.password_reset_done, name='password_reset_done'),
    url(_(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'),
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(_(r'^password/reset/complete/$'), auth_views.password_reset_complete, name='password_reset_complete'),

    # user registration
    url(_(r'^register/$'), RegistrationView.as_view(), name='registration_register'),
    url(_(r'^register/complete/$'), TemplateView.as_view(template_name='registration/registration_complete.html'),
        name='registration_complete'),
    url(_(r'^activate/complete/$'), TemplateView.as_view(template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    url(_(r'^activate/(?P<activation_key>\w+)/$'), ActivationView.as_view(), name='registration_activate'),
    url(_(r'^register/closed/$'), TemplateView.as_view(template_name='registration/registration_closed.html'),
        name='registration_disallowed'),

    # langage switcher
    url(r'^i18n/(?P<language>\w+)/$', 'core.views.i18n_switcher', name='i18n_switcher'),

    url(r'^admin/', include(admin.site.urls)),
]
