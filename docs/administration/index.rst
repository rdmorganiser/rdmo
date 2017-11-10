Administration
==============

The Django framework offers a rich administration (or short admin) interface, which allows you to directly manipulate most of the entries in the database directly. Obviously, only users with the correct permissions are allowed to use this interface. The user created during the installation process using ``./manage.py createsuperuser`` has this *superuser* status.

The admin interface is avalable under the link *Admin* in the navigation bar. It will only be needed on rare ocasion, since most the configuration of the questionaire and the other functions of RDMO can be done using the more user-friendly Management interface described :doc:`in the following chapter of this documantation </management/index>`.

That being said, the admin interface is needed, especially after installation, to set the title and URL of the :doc:`site <site>`, to configure :doc:`users and groups <users>`, to configure the connection to :doc:`OAUTH providers <allauth>`, and to create :doc:`tokens <tokens>` to be used with the API.

.. toctree::
   :caption: Index
   :maxdepth: 2

   site
   users
   allauth
   tokens
