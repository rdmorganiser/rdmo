Figures
=======

Below is a graphical representation of the different models in rdmo, created with ``graphviz``:

.. image:: ../_static/img/models.png
   :target: ../_static/img/models.png

To create/update the figure, install `graphviz`:

.. code:: bash

    apt-get install graphviz-dev
    pip install pygraphviz


Then create the image using:

.. code:: bash

    ./manage.py graph_models \
        accounts conditions domain options questions projects tasks views \
        -g > docs/img/models.dot

    dot -Tsvg -o docs/img/models.svg docs/img/models.dot
    dot -Tpdf -o docs/img/models.pdf docs/img/models.dot
    dot -Tpng -o docs/img/models.png docs/img/models.dot
