nginx and gunicorn
------------------

As mentioned several times, you should create a dedicated user for RDMO. All steps for the installation, which do not need root access, should be done using this user. Here we assume this user is called ``rdmo`` and it's home is ``/srv/rdmo`` and therefore your ``rdmo-app`` is located in ``/srv/rdmo/rdmo-app``.

First install gunicorn inside your virtual environment:

.. code:: bash

    pip install -r requirements/gunicorn.txt

Then, test ``gunicorn`` using:

.. code:: bash

    gunicorn --bind 0.0.0.0:8000 config.wsgi:application

This should serve the application like ``runserver``, but without the static assets, like CSS files and images. After the test kill the ``gunicorn`` process again.

Now, create a systemd service file for RDMO. Systemd will launch the gunicorn process on startup and keep running. Create a new file in `/etc/systemd/system/rdmo.service` and enter:

::

    [Unit]
    Description=RDMO gunicorn daemon
    After=network.target

    [Service]
    User=rdmo
    Group=rdmo
    WorkingDirectory=/srv/rdmo/rdmo-app
    ExecStart=/srv/rdmo/rdmo-app/env/bin/gunicorn --workers 2 --bind unix:/srv/rdmo/rdmo.sock config.wsgi:application

    [Install]
    WantedBy=multi-user.target

This service needs to be started and enables like any other service:

.. code:: bash

    systemctl start rdmo
    systemctl enable rdmo

Next, install nginx

.. code:: bash

    apt-get install nginx  # debian/Ubuntu
    yum install nginx      # CentOS

Edit the nginx configuration (in ``/etc/nginx/sites-available/default`` or ``/etc/nginx/conf.d/vhost.conf``) as follows:

::

    server {
        listen 80;
        server_name YOURDOMAIN;

        location / {
            proxy_pass http://unix:/srv/rdmo/rdmo.sock;
        }
        location /static/ {
            alias /srv/rdmo/rdmo-app/static_root/;
        }
    }

Restart nginx. Note that the unix socket ``/srv/rdmo/rdmo.sock`` needs to be accessible by nginx.
