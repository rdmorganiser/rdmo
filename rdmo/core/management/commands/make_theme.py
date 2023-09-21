from pathlib import Path
from shutil import copyfile

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def setup(self, options):
        self.theme_name = options['name']
        self.theme_path = Path(options['name'])
        self.rdmo_path = Path(apps.get_app_config('rdmo').path)
        self.local_path = Path().cwd() / 'config' / 'settings' / 'local.py'

    def copy(self, path):
        source_path = self.rdmo_path / path
        target_path = self.theme_path / Path(*path.parts[1:])

        if target_path.exists():
            print(f'Skip {source_path} -> {target_path}. Target file exists.')
        else:
            print(f'Copy {source_path} -> {target_path}.')

            target_path.parent.mkdir(parents=True, exist_ok=True)
            copyfile(source_path, target_path)

    def enable_theme(self):
        settings_line = f'INSTALLED_APPS = [\'{self.theme_name}\'] + INSTALLED_APPS'
        replaced = False

        local_settings = self.local_path.read_text().splitlines()
        for i, line in enumerate(local_settings):
            if line == settings_line:
                # return if the line is already there
                return

            if line == '# ' + settings_line:
                local_settings[i] = settings_line
                replaced = True

        if not replaced:
            local_settings.append('')
            local_settings.append(settings_line)
            local_settings.append('')

        self.local_path.write_text('\n'.join(local_settings))

    def add_arguments(self, parser):
        parser.add_argument('--name', action='store', default='rdmo_theme',
                            help='Module name for the theme.')
        parser.add_argument('--file', action='store',
                            help='Copy specific file/template, e.g. core/static/css/variables.scss.')

    def handle(self, *args, **options):
        self.setup(options)

        if options['file']:
            self.copy(Path(options['file']))
        else:
            self.theme_path.mkdir(exist_ok=True)
            self.theme_path.joinpath('__init__.py').touch()
            self.theme_path.joinpath('locale').mkdir(exist_ok=True)

            self.copy(Path('core') / 'static' / 'core' / 'css' / 'variables.scss')

            for language, language_string in settings.LANGUAGES:
                self.copy(Path('core') / 'templates' / 'core' / f'home_text_{language}.html')
                self.copy(Path('core') / 'templates' / 'core' / f'about_text_{language}.html')
                self.copy(Path('core') / 'templates' / 'core' / f'footer_text_{language}.html')

            print('Enable theme by adding the necessary config line.')
            self.enable_theme()

        print('Done')
