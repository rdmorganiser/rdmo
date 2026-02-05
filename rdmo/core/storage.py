from django.conf import settings
from django.contrib.staticfiles.storage import StaticFilesStorage

from rdmo import __version__


class VersionedStaticFilesStorage(StaticFilesStorage):

    def url(self, name):
        url = super().url(name)

        if settings.DEBUG:
            return url
        else:
            if '?' in url:
                return f'{url}&v={__version__}'
            else:
                return f'{url}?v={__version__}'
