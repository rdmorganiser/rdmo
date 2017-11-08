Logging
-------

Logging in Django can be very complex and is covered extensively in the `Django documentation <https://docs.djangoproject.com/en/1.11/topics/logging/>`_. For a suitable logging of RDMO you can add the following to your ``config/settings/local.py``:

.. code:: python

    import os
    from . import BASE_DIR

    LOGGING_DIR = '/var/log/rdmo/'
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue'
            }
        },
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s: %(message)s'
            },
            'name': {
                'format': '[%(asctime)s] %(levelname)s %(name)s: %(message)s'
            },
            'console': {
                'format': '[%(asctime)s] %(message)s'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'error_log': {
                'level': 'ERROR',
                'class':'logging.FileHandler',
                'filename': os.path.join(LOGGING_DIR, 'error.log'),
                'formatter': 'default'
            },
            'rdmo_log': {
                'level': 'DEBUG',
                'class':'logging.FileHandler',
                'filename': os.path.join(LOGGING_DIR, 'rdmo.log'),
                'formatter': 'name'
            },
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
                'formatter': 'console'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            'django.request': {
                'handlers': ['mail_admins', 'error_log'],
                'level': 'ERROR',
                'propagate': True
            },
            'rdmo': {
                'handlers': ['rdmo_log'],
                'level': 'DEBUG',
                'propagate': False
            }
        }
    }

This produces two logs:

* ``/var/log/rdmo/error.log`` will contain exception messages from application errors (status code: 500). The messages is the same that ist shown when ``DEBUG = True``, which should not be the case in a production environment. In addition to the log entry, an email is send to all admins specified in the ``ADMINS`` setting.
* ``/var/log/rdmo/rdmo.log`` will contain additional logging information from the RDMO code.
