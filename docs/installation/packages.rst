Install python packages
-----------------------

After you have obtained the ``rdmo-app``, you need to install the ``rdmo`` package and the other python dependencies.

Change to the ``rdmo-app`` directory and create a `virtualenv <https://virtualenv.readthedocs.org>`_ (this is done as your user or the created ``rdmo`` user, not as ``root``):

.. code:: bash

    cd rdmo-app

    python3 -m venv env                                        # for python3
    virtualenv env                                             # for python2.7

    source env/bin/activate                                    # on Linux or macOS
    call env\Scripts\activate.bat                              # on Windows

    pip install --upgrade pip setuptools                       # update pip and setuptools

After the virtual environment is activated, the ``rdmo`` package can be installed using ``pip``:

.. code:: bash

    pip install rdmo

On windows, pandoc needs to be installed in an additional step:

.. code:: bash

    # only on Windows
    python -c "import pypandoc; pypandoc.download_pandoc()"

The virtual environment encapsulates your RDMO installation from the rest of the system. This makes it possible to run several applications with different python dependencies on one machine and to install the dependencies without root permissions.

**Important:** The virtual enviroment needs to be activated, using ``source env/bin/activate`` or ``call env\Scripts\activate.bat``, everytime a new terminal is used.
