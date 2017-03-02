RDMO - Research Data Management Organiser
=========================================

[![Build Status](https://travis-ci.org/rdmorganiser/rdmo.svg?branch=master)](https://travis-ci.org/rdmorganiser/rdmo)
[![Coverage Status](https://coveralls.io/repos/rdmorganiser/rdmo/badge.svg?branch=master&service=github)](https://coveralls.io/github/rdmorganiser/rdmo?branch=master)

This project is currently in an early stage of development and by no means production ready.

More information will follow.

Setup
-----

The setup on different platforms is covered in seperate documents:

* [Setup RDMO on Linux](docs/setup-linux.md)
* [Setup RDMO on OSX](docs/setup-osx.md)
* [Setup RDMO on Windows](docs/setup-windows.md)

Development server
------------------

The Django development server can be started using:

```
./manage.py runserver
```

Then, navigate to `http://localhost:8000` in your browser.

Production setup
----------------

The development server is **not** suited to serve the application to the internet. Hosting RDMO on an actual webserver is covered on a [separate page](docs/production-setup.md).

Testing
-------

For running the test suite use:

```
./manage.py test
```

For a coverage report use:

```
./manage.py coverage
./manage.py coverage --html  # for an HTML coverage report
```

The HTML report can be viewed by opening `htmlcov/index.html` in a browser.


i18n
----

To update the locale files automatiacally run:

```
./manage.py makemessages -a --ignore=env/* --ignore=htmlcov/*
```

Then, edit the `.po` files in the `locale` directory. Afterwards run

```
./manage.py compilemessages
```

Graph models
------------

To create/update the graphical representation of the datamodel, install `graphviz`:

On debian/Ubuntu systems, install a few prerequisites:

```
apt-get install graphviz-dev
pip install pygraphviz
```

Then create the image using:

```
./manage.py graph_models accounts conditions domain options questions projects tasks views \
    -g > docs/figures/models.dot

dot -Tsvg -o docs/figures/models.svg docs/figures/models.dot
dot -Tpdf -o docs/figures/models.pdf docs/figures/models.dot
dot -Tpng -o docs/figures/models.png docs/figures/models.dot
```
