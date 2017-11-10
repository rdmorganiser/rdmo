Development server
------------------

Django comes with an integrated development server. It can be started using:

.. code:: bash

    python manage.py runserver

Then, RDMO is available on http://localhost:8000 in your (local) browser. The development server is **not** suited to serve the application to the internet.

If you want the development server to be accessible from other machines you need to use:

.. code:: bash

    python manage.py runserver 0.0.0.0:8000

where ``8000`` is the port and can be changed according to your needs. Please do not use this setup for more than testing and development, it is not secure.

More information about the development server can be found in the `Django documentation <https://docs.djangoproject.com/en/1.10/intro/tutorial01/#the-development-server>`_.
