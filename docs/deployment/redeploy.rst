Deploy script
~~~~~~~~~~~~~

In order to apply changes to the RDMO code (e.g. after a ``git pull``) the webserver
needs to be reloaded or the ``rdmo/wsgi.py`` file needs to apear modified. This can be done using the ``touch`` command:

.. code:: bash

    touch rdmo/wsgi.py

Also, the ``collectstatic`` command has to be executed again. Both can be achived using:

.. code:: bash

    python manage.py deploy
