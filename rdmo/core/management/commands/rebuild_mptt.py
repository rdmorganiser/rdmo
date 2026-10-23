from django.core.management.base import BaseCommand

from rdmo.domain.models import Attribute
from rdmo.projects.models import Project


class Command(BaseCommand):

    def handle(self, *args, **options):
        Attribute.objects.rebuild()
        Project.objects.rebuild()
