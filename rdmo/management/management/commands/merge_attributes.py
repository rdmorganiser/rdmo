import logging

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext_lazy as _

from rdmo.management.merge_attributes import ReplaceAttributeOnElements

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            help='The URI of the source attribute that will be replaced by the target and will be deleted')
        parser.add_argument(
            '--target',
            help='The URI of the target attribute that will be used to replaced the source')
        parser.add_argument(
            '--save',
            action='store_true',
            help='If specified, the changes will be saved and the source attribute will be deleted. If not specified, the command will do a dry run.'  # noqa: E501
        )

    def handle(self, *args, **options):
        try:
            ReplaceAttributeOnElements(
                source=options['source'],
                target=options['target'],
                save=options['save'],
                verbosity=options['verbosity']
            )
        except ValueError as e:
            raise CommandError(e) from e
        except Exception as e:
            raise CommandError(_('There was an unknown error in calling the command. %s') % e) from e
