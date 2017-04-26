from django.conf.urls import include, url
from django.contrib import admin

from apps.core.views import home, i18n_switcher

from apps.accounts.urls import accounts_patterns, accounts_patterns_api
from apps.conditions.urls import conditions_patterns, conditions_patterns_internal, conditions_patterns_api
from apps.domain.urls import domain_patterns, domain_patterns_internal, domain_patterns_api
from apps.options.urls import options_patterns, options_patterns_internal, options_patterns_api
from apps.projects.urls import projects_patterns, projects_patterns_internal, projects_patterns_api
from apps.questions.urls import questions_patterns, questions_patterns_internal, questions_patterns_api
from apps.tasks.urls import tasks_patterns, tasks_patterns_internal, tasks_patterns_api
from apps.views.urls import views_patterns, views_patterns_internal, views_patterns_api


urlpatterns = [
    url(r'^$', home, name='home'),

    # apps
    url(r'^account/', include(accounts_patterns)),
    url(r'^conditions/', include(conditions_patterns)),
    url(r'^domain/', include(domain_patterns)),
    url(r'^options/', include(options_patterns)),
    url(r'^projects/', include(projects_patterns)),
    url(r'^questions/', include(questions_patterns)),
    url(r'^tasks/', include(tasks_patterns)),
    url(r'^views/', include(views_patterns)),

    # internal AJAX API
    url(r'^api/internal/conditions/', include(conditions_patterns_internal, namespace='internal-conditions')),
    url(r'^api/internal/domain/', include(domain_patterns_internal, namespace='internal-domain')),
    url(r'^api/internal/options/', include(options_patterns_internal, namespace='internal-options')),
    url(r'^api/internal/projects/', include(projects_patterns_internal, namespace='internal-projects')),
    url(r'^api/internal/questions/', include(questions_patterns_internal, namespace='internal-questions')),
    url(r'^api/internal/tasks/', include(tasks_patterns_internal, namespace='internal-tasks')),
    url(r'^api/internal/views/', include(views_patterns_internal, namespace='internal-views')),

    # programmable API
    url(r'^api/v1/accounts/', include(accounts_patterns_api, namespace='api-v1-accounts')),
    url(r'^api/v1/conditions/', include(conditions_patterns_api, namespace='api-v1-conditions')),
    url(r'^api/v1/domain/', include(domain_patterns_api, namespace='api-v1-domain')),
    url(r'^api/v1/options/', include(options_patterns_api, namespace='api-v1-options')),
    url(r'^api/v1/projects/', include(projects_patterns_api, namespace='api-v1-projects')),
    url(r'^api/v1/questions/', include(questions_patterns_api, namespace='api-v1-questions')),
    url(r'^api/v1/tasks/', include(tasks_patterns_api, namespace='api-v1-tasks')),
    url(r'^api/v1/views/', include(views_patterns_api, namespace='api-v1-views')),

    # langage switcher
    url(r'^i18n/([a-z]{2})/$', i18n_switcher, name='i18n_switcher'),

    url(r'^admin/', include(admin.site.urls)),
]
