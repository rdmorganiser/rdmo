Themes
------

RDMO allows for a high level of customization by modifiing the Django *templates* as well as the static assets (CSS file, images, etc.). Django which RDMO is base on offers a powerful method for this. Inside your ``rdmo-app`` directory you can create a ``theme`` folder with a ``static`` and a ``templates`` directory inside:

.. code:: python

    mkdir theme
    mkdir theme/static
    mkdir theme/templates

Then add:

.. code:: python

    THEME_DIR = os.path.join(BASE_DIR, 'theme')

to your ``config/settings/local.py``.

Templates and static files in the ``theme`` directory override files from RDMO as long as they have the same relative path, e.g. the file ``theme/templates/core/base_navigation.html`` overrides ``rdmo/core/templates/core/base_navigation.html``.

Some files you might want to override are:

SASS variables
    ``rdmo/core/static/core/css/variables.scss`` can be copied to ``theme/static/css/variables.scss`` and be used to customize colors.

Navigation bar
    ``rdmo/core/templates/core/base_navigation.html`` can be copied to ``theme/templates/core/base_navigation.html`` and be used to customize the navbar.

Home page text
    ``rdmo/core/templates/core/home_text_en.html`` and ``rdmo/core/templates/core/home_text_de.html`` can be copied to ``theme/templates/core/home_text_en.html`` and ``theme/templates/core/home_text_de.html`` and be used to customize text on the home page.

Note that updates to the RDMO package might render your theme incompatible to the RDMO code and cause errors. In this case the files in ``theme`` need to be adjusted to match their RDMO counterparts in functionality.
