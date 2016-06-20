from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import views as auth_views

from .views import profile_update


urlpatterns = [
    # edit own profile
    url(r'^$', profile_update, name='profile_update'),

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

]
