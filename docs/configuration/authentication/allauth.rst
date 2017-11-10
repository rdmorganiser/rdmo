django-allauth
~~~~~~~~~~~~~~

RDMO uses the excellent `django-allauth <http://www.intenct.nl/projects/django-allauth>`_ as its main authorization library. It enables workflows for user registration and password retrieval, as well as authentication from 3rd party sites using OAUTH2.

Accounts
````````

To enable regular accounts in RDMO add:

.. code:: python

    from rdmo.core.settings import INSTALLED_APPS, AUTHENTICATION_BACKENDS

    ACCOUNT = True
    ACCOUNT_SIGNUP = True

    INSTALLED_APPS += [
        'allauth',
        'allauth.account',
    ]

    AUTHENTICATION_BACKENDS.append('allauth.account.auth_backends.AuthenticationBackend')

to your ``config/settings/local.py``. The setting ``ACCOUNT = True`` enables the general django-allauth features in RDMO, while ``ACCOUNT_SIGNUP = True`` enables new users to register with your RDMO instance. The last lines enable django-allauth to be used by RDMO.

The behavior of ``django-allauth`` can be further configured by the settings documented in the `django-allauth documentation <http://django-allauth.readthedocs.io/en/latest/configuration.html>`_. RDMO sets a few default which can be found in ``config/settings/base.py``.


Social accounts
```````````````

In order to use 3rd party accounts (facebook, github, etc.) with RDMO add:

.. code:: python

    from rdmo.core.settings import INSTALLED_APPS, AUTHENTICATION_BACKENDS

    ACCOUNT = True
    ACCOUNT_SIGNUP = True
    SOCIALACCOUNT = True

    INSTALLED_APPS += [
        'allauth',
        'allauth.account',
        'allauth.socialaccount'
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.github',
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.orcid',
        'allauth.socialaccount.providers.twitter',
        ...
    ]

    AUTHENTICATION_BACKENDS.append('allauth.account.auth_backends.AuthenticationBackend')

to your ``config/settings/local.py``. The setting ``SOCIALACCOUNT = True`` is used by RDMO to show certain parts of the user interface connected to 3rd party accounts, while as before, the lines after ``INSTALLED_APPS`` enable the feature to be used by RDMO. Each provider has a seperate app you need to add to ``INSTALLED_APPS``. A list of all providers supported by django-allauth can be found `here <http://django-allauth.readthedocs.io/en/latest/providers.html>`_.

Once the installation is complete, the credentials of your OAUTH provider need to be entered in the admin interface. This is covered in the :doc:`administration chapter </administration/allauth>` of this documentation.
