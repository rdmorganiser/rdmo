LDAP
~~~~

In order to use an LDAP backend with RDMO you need to install some prerequistes

.. code:: bash

    sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev  # for debian/Ubuntu

In the virtual environment created for RDMO do:

.. code:: bash

    pip install -r requirements/ldap.txt

LDAP installations can be very different and we only discuss one particular example using [freeipa](http://www.freeipa.org/page/HowTo/LDAP). We assume that the LDAP service is running on ``ldap.example.com``. RDMO needs a *System Account*. In order to create it, run:

.. code:: bash

    ldapmodify -x -D 'cn=Directory Manager' -W

and type in:

::

    dn: uid=system,cn=sysaccounts,cn=etc,dc=example,dc=com
    changetype: add
    objectclass: account
    objectclass: simplesecurityobject
    uid: rdmo
    userPassword: YOURPASSWORD
    passwordExpirationTime: 20380119031407Z
    nsIdleTimeout: 0

and end with a blank line followed by <kbd>ctrl</kbd>-<kbd>d</kbd>.

Then, add

.. code:: python

    import ldap
    from django_auth_ldap.config import LDAPSearch

    AUTH_LDAP_SERVER_URI = "ldap://ldap.example.com"
    AUTH_LDAP_BIND_DN = "uid=rdmo,dc=vbox"
    AUTH_LDAP_BIND_PASSWORD = "YOURPASSWORD"
    AUTH_LDAP_USER_SEARCH = LDAPSearch("cn=users,cn=accounts,dc=vbox", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

    AUTH_LDAP_USER_ATTR_MAP = {
        "first_name": "givenName",
        "last_name": "sn",
        'email': 'mail'
    }

to your ``rdmo/settings/local.py``.
