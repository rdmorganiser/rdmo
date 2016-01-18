from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from registration.backends.default.views import RegistrationView, ActivationView

urlpatterns = [
    # /accounts/
    url(r'^$', 'apps.accounts.views.profile_update', name='profile_update'),

    # /accounts/password/change
    url(r'^%s/%s/$' % (_('password'), _('change')),
        auth_views.password_change,
        {
            'template_name': 'accounts/password_change_form.html'
        },
        name='password_change'),

    # /accounts/password/change/done
    url(r'^%s/%s/%s/$' % (_('password'), _('change'), _('done')),
        auth_views.password_change_done,
        {
            'template_name': 'accounts/password_change_done.html'
        },
        name='password_change_done'),

    # /accounts/password/reset/
    url(r'^%s/%s/$' % (_('password'), _('reset')),
        auth_views.password_reset,
        {
            'template_name': 'accounts/password_reset_form.html',
            'email_template_name': 'accounts/password_reset_email.txt',
            'subject_template_name': 'accounts/password_reset_subject.txt',
        },
        name='password_reset'),

    # /accounts/password/reset/done/
    url(r'^%s/%s/%s/$' % (_('password'), _('reset'), _('done')),
        auth_views.password_reset_done,
        {
            'template_name': 'accounts/password_reset_done.html'
        },
        name='password_reset_done'),

    # /accounts/password/<uidb64>/<token>/
    url(r'^%s/%s/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$' % (_('password'), _('reset')),
        auth_views.password_reset_confirm,
        {
            'template_name': 'accounts/password_reset_confirm.html',
        },
        name='password_reset_confirm'),

    # /accounts/password/reset/complete/
    url(r'^%s/%s/%s/$' % (_('password'), _('reset'), _('complete')),
        auth_views.password_reset_complete,
        {
            'template_name': 'accounts/password_reset_complete.html',
        },
        name='password_reset_complete'),

    # /accounts/register/
    url(r'^%s/$' % _('register'), RegistrationView.as_view(), name='registration_register'),

    # /accounts/register/complete/
    url(r'^%s/%s/$' % (_('register'), _('complete')),
        TemplateView.as_view(template_name='registration/registration_complete.html'),
        name='registration_complete'),

    # /accounts/activate/complete/
    url(r'^%s/%s/$' % (_('activate'), _('complete')),
        TemplateView.as_view(template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),

    # /accounts/activate/<activation_key>/
    url(r'^%s/(?P<activation_key>\w+)/$' % _('activate'),
        ActivationView.as_view(),
        name='registration_activate'),

    # /accounts/register/closed/
    url(r'^%s/%s/$' % (_('register'), _('closed')),
        TemplateView.as_view(template_name='registration/registration_closed.html'),
        name='registration_disallowed'),
]
