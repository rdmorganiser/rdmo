from django.contrib.auth.models import User
from django.test import TestCase

from test_generator.viewsets import TestReadOnlyModelViewsetMixin

from rdmo.accounts.utils import set_group_permissions


class AccountsViewsetTestCase(TestCase):

    lang = 'en'

    fixtures = (
        'users.json',
        'groups.json',
        'accounts.json'
    )

    users = (
        ('editor', 'editor'),
        ('reviewer', 'reviewer'),
        ('user', 'user'),
        ('api', 'api'),
        ('anonymous', None),
    )

    def setUp(self):
        set_group_permissions()


class UserAPITests(TestReadOnlyModelViewsetMixin, AccountsViewsetTestCase):

    instances = User.objects.all()
    url_names = {
        'viewset': 'api-v1-accounts:user'
    }
    status_map = {
        'list_viewset': {
            'editor': 403, 'reviewer': 403, 'api': 200, 'user': 403, 'anonymous': 403
        },
        'detail_viewset': {
            'editor': 403, 'reviewer': 403, 'api': 200, 'user': 403, 'anonymous': 403
        },
    }
