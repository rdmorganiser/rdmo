Shibboleth
~~~~~~~~~~

In order to use Shibboleth with RDMO it needs to be deployed in a production environment using Apache2. The Setup is documented :doc:`here </deployment/apache>`.

Next, install the Shibboleth Apache module for service providers from your distribution repository, e.g. for Debian/Ubuntu:

.. code:: bash

    sudo apt-get install libapache2-mod-shib2


In addition, `django-shibboleth-remoteuser <https://github.com/Brown-University-Library/django-shibboleth-remoteuser>`_ needs to be installed in your RDMO virtual environment:

.. code:: bash

    pip install -r requirements/shibboleth.txt


Configure your Shibboleth service provider using the files in ``/etc/shibboleth/``. This may vary depending on your Identity Provider. RDMO needs the ``REMOTE_SERVER`` to be set and 4 attributes from your identity provider:

* a username (usually ``eppn``)
* an email address (usually ``mail`` or ``email``)
* a first name (usually ``givenName``)
* a last name (usually ``sn``)

In our test environent this is accomplished by editing ``/etc/shibboleth/shibboleth2.xml``:

.. code:: xml

    <ApplicationDefaults entityID="https://sp.vbox/shibboleth"
                         REMOTE_USER="uid eppn persistent-id targeted-id">


and '/etc/shibboleth/attribute-map.xml':

.. code:: xml

    <Attribute name="urn:oid:0.9.2342.19200300.100.1.1" id="uid"/>
    <Attribute name="urn:oid:2.5.4.4" id="sn"/>
    <Attribute name="urn:oid:2.5.4.42" id="givenName"/>
    <Attribute name="urn:oid:0.9.2342.19200300.100.1.3" id="mail"/>


Restart the Shibboleth service provider demon.

.. code:: bash

    service shibd restart


In your Apache2 virtual host configuration, add:

::

    <Location /Shibboleth.sso>
        SetHandler shib
    </Location>
    <LocationMatch /(account|domain|options|projects|questions|tasks|conditions|views)>
        AuthType shibboleth
        require shibboleth
        ShibRequireSession On
        ShibUseHeaders On
    </LocationMatch>


In your ``config/settings/local.py`` add or uncomment:

.. code:: python

    from rdmo.core.settings import INSTALLED_APPS, AUTHENTICATION_BACKENDS, MIDDLEWARE_CLASSES

    SHIBBOLETH = True
    PROFILE_UPDATE = False

    INSTALLED_APPS += ['shibboleth']

    AUTHENTICATION_BACKENDS.append('shibboleth.backends.ShibbolethRemoteUserBackend')
    MIDDLEWARE_CLASSES.insert(
        MIDDLEWARE_CLASSES.index('django.contrib.auth.middleware.AuthenticationMiddleware') + 1,
        'shibboleth.middleware.ShibbolethRemoteUserMiddleware'
    )

    SHIBBOLETH_ATTRIBUTE_MAP = {
        'uid': (True, 'username'),
        'givenName': (True, 'first_name'),
        'sn': (True, 'last_name'),
        'mail': (True, 'email'),
    }

    LOGIN_URL = '/Shibboleth.sso/Login?target=/projects'
    LOGOUT_URL = '/Shibboleth.sso/Logout'


where the keys of ``SHIBBOLETH_ATTRIBUTE_MAP``, ``LOGIN_URL``, and ``LOGOUT_URL`` need to be modified according to your setup. The setting ``SHIBBOLETH = True`` disables the regular login form in RDMO, and tells RDMO to disable the update form for the user profile so that users cannot update their credentials anymore. The ``INSTALLED_APPS``, ``AUTHENTICATION_BACKENDS``, and ``MIDDLEWARE_CLASSES`` settings enable django-shibboleth-remoteuser to be used with RDMO.

Restart the webserver.

.. code:: bash

    service apache2 restart
