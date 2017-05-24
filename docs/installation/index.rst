Installation
============

We suggest running RDMO on a recent linux distribution. We tested CentOS7, debian 8 (Jessie), and Ubuntu 14.04 and 16.04. For development or testing purposes on macOS and Windows is possible. RDMO is mainly written in Python and should work with a Python 2 (version > 2.7) as well as Python 3 (version > 3.4).

Ouside of production, RDMO can be installed using your regular user. In production, a dedicated user should be used. We suggest to create a user called ``rdmo`` with the group ``rdmo`` and the home directory ``/srv/rdmo``. We will use this user throughout the whole documantation.

Do not use the ``root`` user to run RDMO. It is a bad idea anyway and several steps of the installation will not work. ``sudo`` is used in the installation when needing root-privileges to install packages.

.. toctree::
   :maxdepth: 3

   prerequisites
   clone
   dependencies
   setup
   front-end
