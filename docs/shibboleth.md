Shibboleth
==========

In order to use Shibboleth with RDMO it needs to be deployed in a production environment using Apache2. The Setup is documented [here](docs/production-setup.md).

Next install the Shibboleth Apache module for service providers from your distirbutions repository, e.g. for debian/Ubuntu:

```
apt-get install libapache2-mod-shib2
```

In addition, [django-shibboleth-remoteuser](https://github.com/Brown-University-Library/django-shibboleth-remoteuser) needs to be installed in your RDMO virtual environment:

```
pip install -r requirements/shibboleth.txt
```

Configure your Shibboleth service provider using the files in `/etc/shibboleth/`. This may vary depending on your Identity Provider. RDMO needs the `RDMOTE_SERVER` to be set and 4 attributes from your identity provider:

* a username (usually `eppn`)
* an email address (usually `mail` or `email`)
* a first name (usually `givenName`)
* a last name (usually `sn`)

In our test environent this is accomplished by editing '/etc/shibboleth/shibboleth2.xml':

```
<ApplicationDefaults entityID="https://sp.vbox/shibboleth"
                     REMOTE_USER="uid eppn persistent-id targeted-id">
```

and '/etc/shibboleth/attribute-map.xml':

```
<Attribute name="urn:oid:0.9.2342.19200300.100.1.1" id="uid"/>
<Attribute name="urn:oid:2.5.4.4" id="sn"/>
<Attribute name="urn:oid:2.5.4.42" id="givenName"/>
<Attribute name="urn:oid:0.9.2342.19200300.100.1.3" id="mail"/>
```

Restart the Shibboleth service provider demon.

```
service shibd restart
```

In your Apache2 virtual host configuration, add:

```
<Location /Shibboleth.sso>
    SetHandler shib
</Location>
<Location />
    AuthType shibboleth
    require shibboleth
    ShibRequireSession On
    ShibUseHeaders On
</Location>
```

In your `rdmo/settings/local.py` add:

```
INSTALLED_APPS += ['shibboleth']
SHIBBOLETH_ATTRIBUTE_MAP = {
    'uid': (True, 'username'),
    'givenName': (True, 'first_name'),
    'sn': (True, 'last_name'),
    'mail': (True, 'email'),
}
```

where the keys of `SHIBBOLETH_ATTRIBUTE_MAP` need to be modified according to your setup.

Restart the webserver.

```
service apache2 restart
```

From now on, you will be directed to your identity provider login when visiting RDMO.

Since you cannot log in using the admin account created with `createsuperuser` anymore, you need to promote your Shibboleth user to superuser status using:

```
./manage.py promote-user-to-superuser YOURUSERNAME
```
