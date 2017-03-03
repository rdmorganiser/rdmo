Install Python dependencies
---------------------------

After you cloned the RDMO repository, change to the created directory, create a `virtualenv <https://virtualenv.readthedocs.org>`_ and install the required dependencies:

.. code:: bash

    cd rdmo
    virtualenv env                                             # for python 2.7
    python -m venv env                                         # for python 3.4

    source env/bin/activate                                    # on Linux or macOS
    call env\Scripts\activate.bat                              # on Windows

    pip install -r requirements/base.txt
    pip install -r requirements/development.txt                # for development
    pip install -r requirements/postgres.txt                   # for PostgreSQL
    pip install -r requirements/mysql.txt                      # for MySQL

    python -c "import pypandoc; pypandoc.download_pypandoc()"  # on Windows
