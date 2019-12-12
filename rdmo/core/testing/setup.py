import pytest
from django.core.management import call_command

from rdmo.accounts.utils import set_group_permissions

fixtures = (
    'groups.json',
    'users.json',
    'accounts.json',
    'domain.json',
    'options.json',
    'conditions.json',
    'questions.json',
    'tasks.json',
    'views.json',
    'projects.json',
)


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        for fixture in fixtures:
            call_command('loaddata', fixture)

        set_group_permissions()
