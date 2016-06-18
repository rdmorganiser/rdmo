DMPwerkzeug
===========

[![Build Status](https://travis-ci.org/DMPwerkzeug/DMPwerkzeug.svg?branch=master)](https://travis-ci.org/DMPwerkzeug/DMPwerkzeug)
[![Coverage Status](https://coveralls.io/repos/DMPwerkzeug/DMPwerkzeug/badge.svg?branch=master&service=github)](https://coveralls.io/github/DMPwerkzeug/DMPwerkzeug?branch=master)

This project is currently in an early stage of development and by no means production ready.

More information will follow.

Setup
-----

The setup on different platforms is covered in seperate documents:

* [Setup DMPwerkzeug on Linux](docs/setup-linux.md)
* [Setup DMPwerkzeug on OSX](docs/setup-osx.md)
* [Setup DMPwerkzeug on Windows](docs/setup-windows.md)

Fixtures
--------

Once the application is set up you can load fixtures with some initial data:

```
./manage.py loaddata fixtures/*
```

Development server
------------------

The Django development server can be started using:

```
./manage.py runserver
```

Then, navigate to `http://localhost:8000` in your browser.

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
./manage.py graph_models accounts domain questions projects -g > docs/models.dot
dot -Tsvg -o docs/models.svg docs/models.dot
dot -Tpdf -o docs/models.pdf docs/models.dot
dot -Tpng -o docs/models.png docs/models.dot
```
