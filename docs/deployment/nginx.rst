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

Now, create a systemd service file for RDMO. Systemd will launch the gunicorn process on startup and keep running. Create a new file in `/etc/systemd/system/rdmo.service` and enter (you will need root/sudo permissions for that):

::

    [Unit]
    Description=RDMO gunicorn daemon
    After=network.target

    [Service]
    User=rdmo
    Group=rdmo
    WorkingDirectory=/srv/rdmo/rdmo-app
    ExecStart=/srv/rdmo/rdmo-app/env/bin/gunicorn --bind unix:/srv/rdmo/rdmo.sock config.wsgi:application

    [Install]
    WantedBy=multi-user.target

This service needs to be started and enables like any other service:

.. code:: bash

    sudo systemctl start rdmo
    sudo systemctl enable rdmo

Next, install nginx

.. code:: bash

    sudo apt install nginx  # on Debian/Ubuntu
    sudo yum install nginx  # on RHEL/CentOS

Edit the nginx configuration as follows (again with root/sudo permissions):

.. code:: bash

    # in /etc/nginx/sites-available/default  on Debian/Ubuntu
    # in /etc/nginx/conf.d/vhost.conf        on RHEL/CentOS
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

Restart nginx. RDMO should now be available on ``YOURDOMAIN``. Note that the unix socket ``/srv/rdmo/rdmo.sock`` needs to be accessible by nginx.

As you can see from the virtual host configurations, the static assets, like CSS and JavaScript files are served independent from the reverse proxy to the gunicorn process. In order to do so they need to be gathered in the ``static_root`` directory. This can be archived by running:

.. code:: bash

    python manage.py collectstatic

in your virtual environment.

In order to apply changes to the RDMO code (e.g. after an :doc:`upgrade </upgrade/index>`) the gunicorn process need to be restarted:

.. code:: bash

    sudo systemctl restart rdmo
