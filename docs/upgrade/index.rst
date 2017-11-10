Upgrade
=======

The ``rdmo`` package can be conveniently upgraded using the ``pip`` command. However, before you perform any changes to your installation, please backup the important components to a save location.

A PostgreSQL or MySQL database can be database can be dumped into a file using:

.. code:: bash

    pg_dump [DBNAME] > rdmo.sql  # PostgreSQL
    mysqldump -uroot -p [DBNAME] > rdmo.sql

Your ``rdmo-app`` directory (including any sqlite3 database) can be copied using the usual commands. Note that your virtual environment will not work after being moved to a different path.

In order to upgrade your RDMO installation go to your ``rdmo-app`` directory, activate your virtual environment, and upgrade the ``rdmo`` package using ``pip``:

.. code:: bash

    pip install --upgrade rdmo

In order to install a specific version (e.g. 0.9.0) of RDMO use:

.. code:: bash

    pip install --upgrade rdmo==0.9.0

After the upgrade a database migration might be necessary:

.. code:: bash

    python manage.py migrate

Please check the release notes if this, or other, steps are necessary.


Upgrade to version 0.9.0
------------------------

With version 0.9.0 we introduced the split into the ``rdmo-app`` and the centrally maintained ``rdmo`` package. Therefore a few additional steps are needed to upgrade any earlier version to 0.9.0 or beyond:

1)  In any case perform a backup of your ``rdmo`` directory and your database as described above.

2)  Perform the steps :doc:`/installation/clone` and :doc:`/installation/packages` as if you would install a new instance of RDMO.

3)  Copy your old configuration from ``/path/to/old/rdmo/rdmo/settings/local.py`` to ``/path/to/new/rdmo-app/config/settings/local.py``. The new ``config`` directory replaces the old ``rdmo`` directory.

4)  If you already have a ``theme`` directory, copy it into the new ``rdmo-app`` folder.

5)  Run a database migration (Unless you skipped several versions, the output should be ``No migrations to apply.``):

    .. code:: bash

        python manage.py migrate

6)  Download the front-end files from the CDN. We don't use bower and npm anymore.

    .. code:: bash

        python manage.py download_vendor_files

7)  Update the path to the ``wsgi.py`` script in your Apache or nginx configuration. It is now under ``/path/to/new/rdmo-app/config/wsgi.py``.

8)  Redeploy RDMO as described under :doc:`/deployment/redeploy`.

If you have trouble with the upgrade process, don't hesitate to contact the RDMO team for support.
