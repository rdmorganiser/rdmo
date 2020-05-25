import base64
import hashlib
import os
import shutil

import requests
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        # remove old vendor files
        vendor_dir = os.path.join(settings.BASE_DIR, 'vendor/')
        try:
            shutil.rmtree(vendor_dir)
        except FileNotFoundError:
            pass

        for key, vendor_conf in settings.VENDOR.items():
            for file_type in ['js', 'css', 'img', 'font']:
                if file_type in vendor_conf:
                    for file in vendor_conf[file_type]:
                        # get the directory and the file_name
                        path_tokens = ['vendor', key] + os.path.normpath(file['path']).split(os.path.sep)
                        directory = os.path.join(*path_tokens[:-1])
                        file_name = os.path.join(*path_tokens)

                        # create the needed diredtories
                        try:
                            os.makedirs(directory)
                        except OSError:
                            pass

                        # get the full url of the file
                        url = requests.compat.urljoin(vendor_conf['url'], file['path'])

                        print('%s -> %s' % (url, file_name))

                        # fetch the file from the cdn
                        response = requests.get(url)
                        response.raise_for_status()
                        with open(file_name, 'wb') as f:
                            f.write(response.content)

                        # check the intergrety of the file if a SRI was supplied
                        if 'sri' in file:
                            algorithm, file_hash = file['sri'].split('-')

                            h = hashlib.new(algorithm)
                            h.update(open(file_name, 'rb').read())
                            if base64.b64encode(h.digest()).decode() != file_hash:
                                raise Exception('Subresource Integrity (SRI) failed for %s' % file_name)
