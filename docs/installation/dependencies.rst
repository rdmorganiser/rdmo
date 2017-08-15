Install Python dependencies
---------------------------

After you have cloned the RDMO repository into the ``rdmo`` directory, change to this directory, create a `virtualenv <https://virtualenv.readthedocs.org>`_ and install the required dependencies (this is done as your user or the created ``rdmo`` user, not as ``root``):

.. code:: bash

    cd rdmo
    virtualenv env                                             # for python 2.7
    python -m venv env                                         # for python 3.4

    source env/Scripts/activate                                # on Linux or macOS
    call env\Scripts\activate.bat                              # on Windows

    pip install -r requirements/base.txt

    python -c "import pypandoc; pypandoc.download_pandoc()"    # on Windows

The virtual environment encapsulates your RDMO installation from the rest of the system. This makes it possible to run several applications with different python dependencies on one machine and to install the dependencies without root permissions.

**Important:** The virtual enviroment needs to be activated, using ``source env/bin/activate`` or ``call env\Scripts\activate.bat``, everytime e new terminal is used.
