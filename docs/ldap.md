LDAP
====

Installation
------------

Install prerequisites:

```
sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev  # for debian/Ubuntu
```

In the virtual environment you created for RDMO:

```
pip install -r requirements/ldap.txt
```

Setup
-----

In your LDAP server, add a *System Account* for RDMO. For [freeipa](http://www.freeipa.org/page/HowTo/LDAP)) run:

```
ldapmodify -x -D 'cn=Directory Manager' -W
```

and type in:

```
dn: uid=system,cn=sysaccounts,cn=etc,dc=example,dc=com
changetype: add
objectclass: account
objectclass: simplesecurityobject
uid: rdmo
userPassword: YOURPASSWORD
passwordExpirationTime: 20380119031407Z
nsIdleTimeout: 0
```

and end with a blank line followed by <kbd><kbd>ctrl</kbd>-<kbd>d</kbd></kbd>.

Then, add:

```
import ldap
from django_auth_ldap.config import LDAPSearch

AUTH_LDAP_SERVER_URI = "ldap://ipa.vbox"
AUTH_LDAP_BIND_DN = "uid=rdmo,dc=vbox"
AUTH_LDAP_BIND_PASSWORD = "YOURPASSWORD"
AUTH_LDAP_USER_SEARCH = LDAPSearch("cn=users,cn=accounts,dc=vbox", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    'email': 'mail'
}
```

to your `rdmo/settings/base.py`.
