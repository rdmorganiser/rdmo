#!/usr/bin/env python
import argparse
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def main():
    parser = argparse.ArgumentParser(description='Run the tests for RDMO.')
    parser.add_argument('-k', '--keepdb', action='store_true', help='Preserves the test database between runs.')

    args = parser.parse_args()

    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

    django.setup()
    TestRunner = get_runner(settings)
    failures = TestRunner(verbosity=1, keepdb=args.keepdb).run_tests([])
    sys.exit(bool(failures))


if __name__ == "__main__":
    main()
