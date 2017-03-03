Install front-end components
----------------------------

Finally, install the front-end components. This can be done using bower:

.. code:: bash

    python manage.py bower install


but only I node.js, npm and bower were installed before. If node.js is not available or not wanted on the machine, you can download the components using `wget` from a different repository:

.. code:: bash

    wget -qO- https://github.com/rdmorganiser/rdmo-components/archive/master.tar.gz | tar xvz
    mv rdmo-components-master components_root

In both cases a ``components_root/bower_components`` containing various JavaScript and CSS libraries should be available.
