Collect static files
--------------------

As you can see from the virtual host configurations, the static assets, like CSS and JavaScript files are served independent from the WSGI-python script. In order to do so they need to be gathered in the ``static_root`` directory. This can be archived by running:

.. code:: bash

    python manage.py collectstatic
