Deployment
==========

As already mentioned, RDMO can be run in two different setups:

* for :doc:`development or testing <development>`, using the build-in Django development server.

* in production, using a web server and the `wsgi <https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/>`_ protocoll. We suggest to use one of the two following setups:

    * :doc:`Apache2 and mod_wsgi <apache>`
    * :doc:`nginx, gunicorn and systemd <nginx>`

.. toctree::
   :caption: Index
   :maxdepth: 2

   development
   apache
   nginx
