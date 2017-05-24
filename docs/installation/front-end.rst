Install front-end components
----------------------------

Finally, install the front-end components (JavaScript and CSS libraries). This can be done in two ways: just downloading the files or using bower.

Download files
~~~~~~~~~~~~~~

The front-end components can be downloaded using ``wget`` from a different repository. After download, they need to be extracted into a directory ``components_root/bower_components``:

.. code:: bash

    wget -qO- https://github.com/rdmorganiser/rdmo-components/archive/master.tar.gz | tar xvz
    mv rdmo-components-master components_root


Bower
~~~~~

The usage of bower is more convenient but requires the installation of node.js:

.. code-block:: bash

    # on debian/Ubuntu
    sudo apt-get install nodejs nodejs-legacy npm
    sudo npm -g install bower

    # on CentOS
    sudo yum install nodejs
    sudo npm install -g bower

    # on macOS
    brew install node
    npm -g install bower

On Windows, you need to:

* download and install node.js from https://nodejs.org/en/download
* after the installation of node.js, install bower using ``npm -g install bower`` in ``cmd.exe``.

Then, the front-side components can be installed (and updated) using:

.. code:: bash

    python manage.py bower install

in your virtual environment.
