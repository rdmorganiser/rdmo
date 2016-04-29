from django.conf.urls import include, url
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth import views as auth_views

handler404 = 'apps.core.views.not_found'

urlpatterns = [
    url(r'^$', 'apps.core.views.home', name='home'),

    # apps
    url(_(r'^account/'), include('apps.accounts.urls')),
    url(_(r'^domain/'), include('apps.domain.urls')),
    url(_(r'^projects/'), include('apps.projects.urls')),
    url(_(r'^questions/'), include('apps.questions.urls')),

    # REST api
    url(r'^api/domain/', include('apps.domain.urls_api')),
    url(r'^api/projects/', include('apps.projects.urls_api')),
    url(r'^api/questions/', include('apps.questions.urls_api')),

    # login and logout
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),

    # langage switcher
    url(r'^i18n/([a-z]{2})/$', 'apps.core.views.i18n_switcher', name='i18n_switcher'),

    url(r'^admin/', include(admin.site.urls)),
]
