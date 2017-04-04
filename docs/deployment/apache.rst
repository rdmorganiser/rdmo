Apache and mod_wsgi
-------------------

In production, you should create a dedicated user for RDMO. All steps for the installation, which do not need root access, should be done using this user. Here we assume this user is called ``rdmo`` and it's home is ``/srv/rdmo`` and RDMO is located in ``/srv/rdmo/rdmo``.

Install the Apache server and ``mod_wsgi`` using:

.. code:: bash

    apt-get install apache2 libapache2-mod-wsgi  # debian/Ubuntu
    yum install httpd mod_wsgi                   # CentOS

and create a virtual host configuration:

::

    <VirtualHost *:80>
        ServerAdmin webmaster@localhost

        DocumentRoot /var/www/html/

        # the css and js files are just served as static files
        Alias /rdmo/static /srv/rdmo/rdmo/static_root/
        <Directory /srv/rdmo/rdmo/static_root/>
            Require all granted
        </Directory>

        WSGIDaemonProcess rdmo user=rdmo group=rdmo processes=2 \
            python-path=/srv/rdmo/rdmo:/srv/rdmo/rdmo/env/lib/python2.7/site-packages
        WSGIProcessGroup rdmo
        WSGIScriptAlias /rdmo /srv/rdmo/rdmo/rdmo/wsgi.py process-group=rdmo

        <Directory /srv/rdmo/rdmo/rdmo/>
            <Files wsgi.py>
                Require all granted
            </Files>
        </Directory>
    </VirtualHost>

Restart the Apache server. Note that the Apache user needs to have access to ``/srv/rdmo/rdmo/static_root/``.
