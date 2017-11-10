Cache
-----

RDMO uses a cache for some of it's pages. In the development setup, this is done using local-memory caching. In production, we suggest using `memcached <https://memcached.org>`_. In order to do this you need to install python-memcached:

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
