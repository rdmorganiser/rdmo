Testing
=======

Setup tests
-----------

First, create a `local.py` file:


```bash
cp testing/config/settings/sample.local.py testing/config/settings/local.py
```

Afterwards edit the `local.py` as for a regular RDMO instance.


Running tests
-------------

```bash
# from the root directory of the rdmo repo
pytest
pytest -x                                                       # stop after the first failed test
pytest --reuse-db                                               # keep the database between test runs
pytest --numprocesses=auto --dist=loadscope                     # run tests in parallel
pytest rdmo/domain                                              # test only the domain app
pytest rdmo/domain/tests/test_viewsets.py                       # run only a specific test file
pytest rdmo/domain/tests/test_viewsets.py::test_attribute_list  # run only a specific test
pytest -k 'test_validator'                                      # run only set of test files, using substring matching
```

Coverage
--------

```bash
pytest --cov                    # show a coverage report in the terminal
pytest --cov --cov-report html  # additionally create a browsable coverage report in htmlcov/
pytest --cov=rdmo/domain        # only compute coverage for the domain app
```


Testing the app
---------------

Tests can also be run from the `rdmo-app`. To do so, create a `pytest.ini` in your `rdmo-app` directory:

```
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
testpaths = tests env/lib/python3.7/site-packages/rdmo
python_files = test_*.py
```

where the path `env/lib/python3.7/site-packages/rdmo` might be adjusted to your system. The path `tests` is the directory in your `rdmo-app` where you can put custom, site-specific tests. Please refer to the [pytest documentation](https://docs.pytest.org/en/latest/assert.html) on how to write tests.

Next, create a file `conftest.py`:

```
import os

import pytest
from django.conf import settings
from django.contrib.admin.utils import flatten
from django.core.management import call_command
from rdmo.accounts.utils import set_group_permissions


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        fixtures = flatten([os.listdir(fixture_dir) for fixture_dir in settings.FIXTURE_DIRS])

        call_command('loaddata', *fixtures)
        set_group_permissions()
```

This file is used to load test data (so called fixtures) into the database before testing. The fixtures reside in a directory `fixtures` in your `rdmo-app`. In order to use the same fixtures as the RDMO repo does, copy all files in https://github.com/rdmorganiser/rdmo/tree/master/testing/fixtures to the local directory `fixtures`. In addition to the fixtures, XML test data needs to provided in a directory `xml`. Similar to before, RDMO test data can be obtained from https://github.com/rdmorganiser/rdmo/tree/master/testing/xml.
