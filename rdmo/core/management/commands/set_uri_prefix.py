from django.core.management.base import BaseCommand

from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute
from rdmo.options.models import Option, OptionSet
from rdmo.questions.models import Catalog, Question, QuestionSet, Section, Subsection
from rdmo.tasks.models import Task
from rdmo.views.models import View


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('uri_prefix', action='store', help='URI prefix to be used for all elements.')

    def handle(self, *args, **options):

        for obj in Condition.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in OptionSet.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in Option.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in Attribute.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in Catalog.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in Section.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in Subsection.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in QuestionSet.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in Question.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in Task.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

        for obj in View.objects.all():
            self._set_uri_prefix(obj, options['uri_prefix'])

    def _set_uri_prefix(self, obj, uri_prefix):
        obj.uri_prefix = uri_prefix
        obj.save()
