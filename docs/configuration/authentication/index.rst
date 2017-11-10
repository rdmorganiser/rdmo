Authentication
--------------

RDMO has three main modes for Authentication:

* Regular user accounts with registration using the :doc:`django-allauth <allauth>` library.
* Using a (read-only) connection to a :doc:`LDAP server <ldap>`
* Installing a :doc:`Shibboleth <shibboleth>` service provider next to RDMO and connect to an identity provider or even a whole Shibboleth federation.

**Important:** These modes are only tested individually and may be treated **mutually exclusive** (unless proven otherwise).

If none of the modes is enabled, only a very basic login will be available and users need to be created using the Django Admin Interface.

.. toctree::
   :hidden:

   allauth
   ldap
   shibboleth
