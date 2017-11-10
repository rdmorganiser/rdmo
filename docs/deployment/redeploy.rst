Deploy script
~~~~~~~~~~~~~

In order to apply changes to the RDMO code (e.g. after an :doc:`upgrade </upgrade/index>`) the webserver
needs to be reloaded or the ``config/wsgi.py`` file needs to apear modified. This can be done using the ``touch`` command:

.. code:: bash

    touch config/wsgi.py

Also, the ``collectstatic`` command has to be executed again. Both can be achived using:

.. code:: bash

    python manage.py deploy

in your virtual environment.