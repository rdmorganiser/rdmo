import os.path
import re
from shutil import copyfile

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def get_folders(self):
        rdmo_core = os.path.join(apps.get_app_config('rdmo').path, 'core')
        rdmo_app_theme = os.path.join(os.getcwd(), 'theme')
        rdmo_app_config = os.path.join(os.getcwd(), 'config', 'settings', 'local.py')
        return rdmo_core, rdmo_app_theme, rdmo_app_config

    def mkdir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def copy(self, source_file):
        fol = self.get_folders()
        source_file = os.path.join(fol[0], source_file)
        target_file = source_file.replace(fol[0], fol[1])
        self.mkdir(re.search(r'.*(?=\/)', target_file).group(0))
        if os.path.exists(target_file) is False:
            print('Copy ' + source_file + ' -> ' + target_file)
            copyfile(source_file, target_file)
        else:
            print('Skip ' + source_file + ' -> ' + target_file + '. Target file exists.')

    def enable_theme(self):
        print('Enable theme by adding the necessary config line')
        rxScheme = r'.*?THEME_DIR.*?=.*?[a-z]'
        replaced = False
        new_arr = []
        fol = self.get_folders()
        with open(fol[2]) as f:
            content = f.read().splitlines()
        for line in content:
            append = True
            if bool(re.search(rxScheme, line)) is True and replaced is True:
                append = False
            if bool(re.search(rxScheme, line)) is True and replaced is False:
                line = 'THEME_DIR = os.path.join(BASE_DIR, \'theme\')'
                replaced = True
            if append is True:
                new_arr.append(line)
                if bool(re.search(rxScheme, line)) is True:
                    replaced = True
        self.write_file(fol[2], new_arr)

    def write_file(self, filename, data):
        with open(filename, 'w') as fp:
            for line in data:
                fp.write(line + '\n')

    def handle(self, *args, **options):
        self.copy(os.path.join('static', 'core', 'css', 'variables.scss'))
        self.copy(os.path.join('templates', 'core', 'base.html'))
        self.copy(os.path.join('templates', 'core', 'base_head.html'))
        self.copy(os.path.join('templates', 'core', 'base_navigation.html'))
        self.copy(os.path.join('templates', 'core', 'base_footer.html'))
        self.enable_theme()
        print('Done')
