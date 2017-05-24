Users and Groups
----------------

The users and groups of your RDMO instance can be managed under **AUTHENTICATION AND AUTHORIZATION**. You can create and update users and set their password directly, but most of the time this will be done by the users themselves using the account menu.

The user created in the installation process can access all features of RDMO. In order to allow other users to access the management or the admin interface, they need to have the needed permissions assigned to them. This can be done in two ways: through groups or using the superuser flag.

Groups
""""""

During the installation, the ``./manage create-groups`` command created 3 groups:

editor
  Users of the group editor can access the :doc:`management interface </management/index>` and can edit all elements of the data model, except the user data entered through the structured inteview.

reviewer
  Users of the group reviewer can access the :doc:`management interface </management/index>`, like editors, but are not allowed to change them (Save will not work). This group can be used to demonstrate the management backend of RDMO to certain users.

api
  Users of the group api can use the programmable API to access all elements of the data model. They will need a :doc:`token <tokens>` to use an api client.

Existing users can be assigned to these groups to gain access to these functions:

1. Click **Users** under **AUTHENTICATION AND AUTHORIZATION** in the admin interface.

2. Click on the user to be changed.

3. Click on the group to be added to the user in the **Available groups** field.

4. Click on the little arrow to move the group to the **Chosen groups** field.

5. Save the user.

Superuser
"""""""""

Superusers have all permissions available and all permission checks will return positive fo them. This does not only allow them to access the management and admin interfaces, but also **access all data from other user** (including the project pages).

To make a user superuser:

1. Click **Users** under **AUTHENTICATION AND AUTHORIZATION** in the admin interface.

2. Click on the user to be changed.

3. Tick the box **Superuser status**.

4. Save the user.
