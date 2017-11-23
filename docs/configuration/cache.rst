Cache
-----

RDMO uses a cache for some of it's pages. In the development setup, this is done using local-memory caching. In production, we suggest using `memcached <https://memcached.org>`_. Memcached can be installed on Debian/Ubuntu using:

.. code:: bash

    sudo apt install memcached

On RHEL/CentOS a few more steps are needed. First install the package using:

.. code:: bash

    sudo yum install memcached

Then edit the settings file to prevent external connections:

.. code:: bash

    # in /etc/sysconfig/memcached
    PORT="11211"
    USER="memcached"
    MAXCONN="1024"
    CACHESIZE="64"
    OPTIONS="-l 127.0.0.1"

Then start the service:

.. code:: bash

    systemctl start memcached
    systemctl enable memcached

Back in your virtual enviroment, you need to install python-memcached:

.. code:: bash

    pip install -r requirements/memcached.txt

and add the following to your ``config/settings/local.py``:

.. code:: python

    CACHES = {
        {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'KEY_PREFIX': 'rdmo_default'
        },
        'api': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'KEY_PREFIX': 'rdmo_api'
        }
    }
