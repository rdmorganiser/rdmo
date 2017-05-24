Apache and mod_wsgi
-------------------

In production, you should create a dedicated user for RDMO. All steps for the installation, which do not need root access, should be done using this user. As before, we assume this user is called ``rdmo`` and it's home is ``/home/rdmo`` and therefore RDMO is located in ``/home/rdmo/rdmo``.

Install the Apache server and ``mod_wsgi`` using:

.. code:: bash

    # debian/Ubuntu
    apt-get install apache2 libapache2-mod-wsgi

    # CentOS
    yum install httpd mod_wsgi

and create a virtual host configuration:

::

    <VirtualHost *:80>
        ServerAdmin webmaster@localhost

        DocumentRoot /var/www/html/

        # the css and js files are just served as static files
        Alias /rdmo/static /home/rdmo/rdmo/static_root/
        <Directory /home/rdmo/rdmo/static_root/>
            Require all granted
        </Directory>

        WSGIDaemonProcess rdmo user=rdmo group=rdmo processes=2 \
            python-path=/home/rdmo/rdmo:/home/rdmo/rdmo/env/lib/python2.7/site-packages
        WSGIProcessGroup rdmo
        WSGIScriptAlias /rdmo /home/rdmo/rdmo/rdmo/wsgi.py process-group=rdmo

        <Directory /home/rdmo/rdmo/rdmo/>
            <Files wsgi.py>
                Require all granted
            </Files>
        </Directory>
    </VirtualHost>

Restart the Apache server. Note that the Apache user needs to have access to ``/home/rdmo/rdmo/static_root/``.
