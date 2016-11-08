Production Setup
----------------

There are several ways to host a Django application like RDMO on a webserver. The
underlying protocoll connecting the webserver is called
[wsgi](https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/). We suggest
two use one of the two following setups:

* Apache and mod_wsgi
* nginx and gunicorn

Both instructions are assuming a Linux system (and some experience with Apache or nginx).

### Apache and mod_wsgi

First install the Apache server and `mod_wsgi`:

```
apt-get install apache2 libapache2-mod-wsgi  # debian/Ubuntu
yum install httpd mod_wsgi                   # CentOS
```

and create a virtual host configuration of the form (RDMO is located in `/srv/rdmo/rdmo`
and belongs to the user `rdmo` of the group `rdmo`):

```
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
```

Then, run

```
python manage.py collectstatic
```

in the RDMO directory to gather all static filed in the `static_root` directory.

Restart the webserver and navigate to its URL.

In order to apply changes to the RDMO code (e.g. after a `git pull`) the webserver
needs to be reloaded or the `rdmo/wsgi.py` file needs to be touched.
