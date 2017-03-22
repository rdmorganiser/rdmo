Setup the application
-----------------

Create a new file ``rdmo/settings/local.py``. You can use ``rdmo/settings/sample.local.py`` as template, i.e.:

.. code:: bash

    cp rdmo/settings/sample.local.py rdmo/settings/local.py    # on Linux or macOS
    copy rdmo\settings\sample.local.py rdmo\settings\local.py  # on Windows

Configure your database connection using the ``DATABASES`` variable in this file. If no ``DATABASE`` setting is given ``sqlite3`` will be used as database backend.

In addition set ``DEBUG = True`` for the development setup.

Then, initialize the database of the application, using:

.. code:: bash

    python manage.py migrate          # initializes the database
    python manage.py createsuperuser  # creates the admin user

