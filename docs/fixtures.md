Fixtures
========

To update the testing data fixtures based on the current database, each of the RDMO apps with new data needs to be dumped using the following command.

```bash
python manage.py dumpdata <app_name> | python -m json.tool --indent 2 > ../rdmo/testing/fixtures/<app_name>.json
```

As an example, the views and projects app contain new data:

```bash
python manage.py dumpdata views | python -m json.tool --indent 2 > ../rdmo/testing/fixtures/views.json
python manage.py dumpdata projects | python -m json.tool --indent 2 > ../rdmo/testing/fixtures/projects.json
```
