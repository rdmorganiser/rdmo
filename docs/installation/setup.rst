Setup the application
---------------------

To set up the application, create a new file ``config/settings/local.py`` in your cloned ``rdmo-app`` directory. For the example user with the home ``/srv/rdmo``, this would now be ``/srv/rdmo/rdmo-app/config/settings/local.py``.

You can use ``config/settings/sample.local.py`` as template, i.e.:

.. code:: bash

    cp config/settings/sample.local.py config/settings/local.py    # on Linux or macOS
    copy config\settings\sample.local.py config\settings\local.py  # on Windows

Most of the settings of your RDMO instance are specified in this file. The different settings are explained in detail :doc:`later in the documentation </configuration/index>`. For a minimal configuration, you need to set ``DEBUG = True`` to see verbose error messages and serve static files, and ``SECRET_KEY`` to a long random string, which you will keep secret. Your database connection is configured using the ``DATABASES`` variable. Database configuration is covered :doc:`later in the documentation </configuration/databases>`. If no ``DATABASE`` setting is given ``sqlite3`` will be used as database backend.

Then, initialize the database of the application, using:

.. code:: bash

    python manage.py migrate                # initializes the database
    python manage.py create_groups          # creates groups with different permissions
    python manage.py createsuperuser        # creates the admin user
    python manage.py download_vendor_files  # dowloads front-end files from the CDN

After these steps, RDMO can be run using Djangos intergrated development server:

.. code:: bash

    python manage.py runserver

Then, RDMO is available on http://127.0.0.1:8000 in your (local) browser. The different ways RDMO can be deployed are covered in the next chapter.
