Deployment
==========

RDMO can be run in two different setups:

* for :doc:`development or testing <development>`, using the build-in Django development server.

* in production, using a web server and the `wsgi <https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/>`_ protocoll. We suggest to use one of the two following setups:

    * :doc:`Apache2 and mod_wsgi <apache>`
    * :doc:`nginx, gunicorn and systemd <nginx>`

  In both cases, the static assets have to be :doc:`collected <collectstatic>` and changes to the code need to be followed by :doc:`re-deploying <redeploy>` RDMO.

.. toctree::
   :caption: Subpages
   :maxdepth: 3

   development
   apache
   nginx
   collectstatic
   redeploy
