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
python --reuse-db                                               # keep the database between test runs
pytest rdmo/domain                                              # test only the domain app
pytest rdmo/domain/tests/test_viewsets.py                       # run only a specific test file
pytest rdmo/domain/tests/test_viewsets.py::test_attribute_list  # run only a specific test
```

Coverage
--------

```bash
pytest --cov                    # show a coverage report in the terminal
pytest --cov --cov-report html  # additionally create a browsable coverage report in htmlcov/
pytest --cov=rdmo/domain        # only compute coverage for the domain app
```
