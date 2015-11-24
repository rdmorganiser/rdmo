from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from registration.backends.default.views import RegistrationView, ActivationView

urlpatterns = [
    # edit own profile
    url(r'^$', 'apps.accounts.views.profile_update', name='profile_update'),

    # change password
    url(_(r'^password/change/$'), auth_views.password_change, {
        'template_name': 'accounts/password_change_form.html'
        }, name='password_change'),
    url(_(r'^password/change/done/$'), auth_views.password_change_done, {
        'template_name': 'accounts/password_change_done.html'
        }, name='password_change_done'),

    # reset password
    url(_(r'^password/reset/$'), auth_views.password_reset, {
        'template_name': 'accounts/password_reset_form.html',
        'email_template_name': 'accounts/password_reset_email.txt',
        'subject_template_name': 'accounts/password_reset_subject.txt',
        }, name='password_reset'),
    url(_(r'^password/reset/done/$'), auth_views.password_reset_done, {
        'template_name': 'accounts/password_reset_done.html',
        }, name='password_reset_done'),
    url(_(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'), auth_views.password_reset_confirm, {
        'template_name': 'accounts/password_reset_confirm.html',
        }, name='password_reset_confirm'),
    url(_(r'^password/reset/complete/$'), auth_views.password_reset_complete, {
        'template_name': 'accounts/password_reset_complete.html',
        }, name='password_reset_complete'),

    # user registration
    url(_(r'^register/$'), RegistrationView.as_view(), name='registration_register'),
    url(_(r'^register/complete/$'), TemplateView.as_view(template_name='registration/registration_complete.html'),
        name='registration_complete'),
    url(_(r'^activate/complete/$'), TemplateView.as_view(template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    url(_(r'^activate/(?P<activation_key>\w+)/$'), ActivationView.as_view(), name='registration_activate'),
    url(_(r'^register/closed/$'), TemplateView.as_view(template_name='registration/registration_closed.html'),
        name='registration_disallowed'),
]
