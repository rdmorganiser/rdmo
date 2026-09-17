import os

from django.conf import settings
from django.contrib.staticfiles.finders import BaseFinder
from django.core.exceptions import SuspiciousFileOperation
from django.core.files.storage import FileSystemStorage
from django.utils._os import safe_join


class StaticRootFinder(BaseFinder):
    """Resolve static files directly from STATIC_ROOT, the way a production web server does."""

    def __init__(self, *args, **kwargs):
        self.storage = FileSystemStorage(location=settings.STATIC_ROOT)
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return []

    def find(self, path, find_all=False):
        try:
            matched = safe_join(settings.STATIC_ROOT, path)
        except SuspiciousFileOperation:
            return [] if find_all else None
        if not os.path.isfile(matched):
            return [] if find_all else None
        return [matched] if find_all else matched

    def list(self, ignore_patterns):
        return iter(())
