'''
Runs rdmo-admin when the rdmo module is run as a script, much like django-admin
(see: https://github.com/django/django/blob/main/django/__main__.py):

    python -m rdmo check

The main method is added as script in pyproject.toml so that

    rdmo-admin check

works as well. Unlike django-admin, a set of generic settings is used for the
management scripts.
'''

import os

from django.core import management

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rdmo.core.management.settings")


def main():
    management.execute_from_command_line()


if __name__ == "__main__":
    main()
