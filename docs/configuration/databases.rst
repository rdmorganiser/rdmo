Databases
---------

RDMO can be used with all database supported by the Django framework. The particular database connection is defined using the setting ``DATABASE``. An overview about the Django database settings is given `here <https://docs.djangoproject.com/en/1.10/ref/settings/#databases>`_. In the following, we show the settings for PostgreSQL, MySQL, and SQLite.

Postgres
````````

In order to use Postgres add the following to your ``rdmo/settings/local.py``:

.. code:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

where ``Name`` is the name of the database, ``USER`` the PostgreSQL user, ``PASSWORD`` her password, ``HOST`` the database host, and ``PORT`` the port PostgreSQL is listening on. Note that, depending on your setup, not all settings are needed. If you are using the peer authentication methods you only need the ``NAME`` and ``ENGINE`` settings.


MySQL
`````

To use MySQL as your database backend add:

.. code:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            'OPTIONS': {
                'unix_socket': '',
            }
        }
    }

to your ``rdmo/settings/local.py``. Here, ``Name`` is the name of the database, ``USER`` the MySQL user, ``PASSWORD`` her password, ``HOST`` the database host, and ``PORT`` the port MySQL is listening on. If you don't use ``/tmp/mysql.sock``, you can use ``unix_socket`` to specify its path.


SQLite
``````

SQLite ist the default option in RDMO and configured in ``rdmo/settings/base.py``. We recommend it only for a development/testing setup. It can be configured in ``rdmo/settings/local.py`` by adding:

.. code:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '',
        }
    }

where ``Name`` is the name of database file.
