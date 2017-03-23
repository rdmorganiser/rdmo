django-allauth
~~~~~~~~~~~~~~

RDMO uses the excellent `django-allauth <http://www.intenct.nl/projects/django-allauth>`_ as its main authorization library. It enables workflows for user registration and password retrieval, as well as authentication from 3rd party sites using OAUTH2.

Accounts
````````

To enable regular accounts in RDMO add:

.. code:: python

    ACCOUNT = True
    ACCOUNT_SIGNUP = True

    INSTALLED_APPS += [
        'allauth',
        'allauth.account',
    ]

    AUTHENTICATION_BACKENDS.append('allauth.account.auth_backends.AuthenticationBackend')

to your ``rdmo/settings/local.py``. The setting ``ACCOUNT = True`` enables the general django-allauth features in RDMO, while ``ACCOUNT_SIGNUP = True`` enables new users to register with your RDMO instance. The last lines enable django-allauth to be used by RDMO.

The behavior of ``django-allauth`` can be further configured by the settings documented in the `django-allauth documentation <http://django-allauth.readthedocs.io/en/latest/configuration.html>`_. RDMO sets a few default which can be found in ``rdmo/settings/base.py``.


Social accounts
```````````````

In order to use 3rd party accounts (facebook, github, etc.) with RDMO `additinally` add:

.. code:: python

    SOCIALACCOUNT = True

    INSTALLED_APPS += [
        'allauth.socialaccount'
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.github',
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.orcid',
        'allauth.socialaccount.providers.twitter',
        ...
    ]

to your ``rdmo/settings/local.py``. The setting ``SOCIALACCOUNT = True`` is used by RDMO to show certain parts of the user interface connected to 3rd party accounts, while, as before, the lines after ``INSTALLED_APPS`` enable the feature to be used by RDMO. Each provider has a seperate app you need to add to ``INSTALLED_APPS``. A list of all providers supported by django-allauth can be found `here <http://django-allauth.readthedocs.io/en/latest/providers.html>`_.

To use an external service with RDMO you also need to register your RDMO site with that service. This process is different from provider to provider. Usually, you need to provide a set of information about your site. Always included is a redirect or callback url. In the following we will use http://127.0.0.1:8000 as an example (which will work on the development server) and you will need to replace that with the correct url of your RDMO application in production.

ORCID
    Login into https://orcid.org and go to the developer tools page at https://orcid.org/developer-tools. Create an app with the Redirect URI

    ::

        http://127.0.0.1:8000/account/orcid/login/callback/

github
    Login into github and go to https://github.com/settings/applications/new and create a new app. Use

    ::

        http://127.0.0.1:8000/account/github/login/callback/

facebook
    Login into facebook and go to https://developers.facebook.com/. Click on the top right menu *My Apps* and choose *Add a new app*. Create a new app. In the following screen choose Facebook login -> Getting started and choose *Web* as the platform. Put in URL under which your application is accessible (Note: 127.0.0.1 will not work here.). Back on the dashboard, go to Settings -> Basic and copy the `App ID` and the `App Secret`.


twitter
    Login into twitter and go to https://apps.twitter.com/app/new and create a new app. Use

    ::

        http://127.0.0.1:8000/account/facebook/login/callback/

    as the Authorized redirect URI. Copy the Client-ID and the Client key.

Google
    Login into google and go to https://console.developers.google.com. Create a new project. After the project is created go to Credentials on the left side and configure the OAuth Authorization screen (second tab). Then create the credentials (first tab), more precise a OAuth Client-ID. Use

    ::

        http://127.0.0.1:8000/account/google/login/callback/

    as the Authorized redirect URI. Copy the Client-ID and the Client key.

To use the registered app in your RDMO application, login in, go to ``Admin / Social applications / Add social application`` and:

1) choose the corresponding provider

2) give a Name of your choice

3) enter the Client ID (or App ID) and the Secret key (or Client secret, Client key, App Secret)

4) Add your site to the chosen sites.
