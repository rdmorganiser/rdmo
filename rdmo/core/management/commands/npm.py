import os
import subprocess

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('command', nargs="*")

    def handle(self, *args, **options):
        nvm_dir = os.getenv('NVM_DIR')

        if nvm_dir is None:
            raise CommandError('NVM_DIR is not set, is nvm.sh installed?')

        if not os.path.exists(nvm_dir):
            raise CommandError('NVM_DIR does not exist, is nvm.sh installed?')

        command = ' '.join(options['command'])
        subprocess.call(['/bin/bash', '-c', f'source {nvm_dir}/nvm.sh; npm {command}'])
