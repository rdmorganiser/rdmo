Themes
------

RDMO allows for a high level of customization by modifiing the Django *templates* as well as the static assets (CSS file, images, etc.). This can be done without forking the repository and modify the code directly. To this purpose create a directory ``theme`` in your ``rdmo`` directory and create a ``static`` and a ``templates`` directory inside:

.. code:: python

    mkdir theme
    mkdir theme/static
    mkdir theme/templates

Then add:

.. code:: python

    THEME_DIR = os.path.join(BASE_DIR, 'theme')

to your ``rdmo/settings/local.py``.

Templates and static files in the ``theme`` directory override file from RDMO as long as they have the same relative path, e.g. the file ``theme/templates/core/base_navigation.html`` overides ``apps/core/templates/core/base_navigation.html``.

Some files you might want to override are:

SASS variables
    ``apps/core/static/core/css/variables.scss`` can be copied to ``theme/static/css/variables.scss`` and used to customize colors.

Navigation bar
    ``apps/core/templates/core/base_navigation.html`` can be copied to ``theme/templates/core/base_navigation.html`` and be used to customize the navbar.

Home page text
    ``apps/core/templates/core/home_text_en.html`` and ``apps/core/templates/core/home_text_de.html`` can be copied to ``theme/templates/core/home_text_en.html`` and ``theme/templates/core/home_text_de.html`` and used to customize text on the home page.

Note that updates to the RDMO repository (e.g. a ``git pull``) might render your theme incompatible to the RDMO code and caus errors. In this case the files in ``theme`` need to be adjusted to match their RDMO counterparts in functionality.
