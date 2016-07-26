from django.test import TestCase
from django.utils import translation
from django.contrib.contenttypes.models import ContentType

from apps.core.testing.mixins import *
from apps.accounts.testing.factories import AdminFactory
from apps.domain.testing.factories import AttributeFactory
from apps.tasks.testing.factories import TaskFactory


from .factories import *


class ConditionTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'conditions:condition'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        task = TaskFactory()
        task_content_type = ContentType.objects.get(app_label='tasks', model='task')
        self.instance = ConditionFactory(content_type=task_content_type, object_id=task.pk)


class AttributeTests(TestModelAPIViewMixin, TestCase):

    api_url_name = 'conditions:attribute'

    def setUp(self):
        translation.activate('en')

        AdminFactory()
        self.client.login(username='admin', password='admin')

        self.instance = AttributeFactory()
