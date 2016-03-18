DMPwerkzeug
===========

[![Build Status](https://travis-ci.org/DMPwerkzeug/DMPwerkzeug.svg?branch=master)](https://travis-ci.org/DMPwerkzeug/DMPwerkzeug)
[![Coverage Status](https://coveralls.io/repos/DMPwerkzeug/DMPwerkzeug/badge.svg?branch=master&service=github)](https://coveralls.io/github/DMPwerkzeug/DMPwerkzeug?branch=master)

This project is currently in an early stage of development and by no means production ready.

More information will follow.


Installation
------------

First, clone the repository to a convenient place:

```
git clone https://github.com/DMPwerkzeug/DMPwerkzeug
```

On debian/Ubuntu systems, install a few prerequisites:

```
apt-get install python-dev python-pip virtualenv npm
npm -g install bower
```

Next, install create a [virtualenv](https://virtualenv.readthedocs.org) and install the required dependecies:

```
cd DMPwerkzeug
virtualenv env                     # for python 2.7
virtualenv --python=python3.4 env  # for python 3.4
source env/bin/activate

pip install -r requirements/base.txt
pip install -r requirements/postgres.txt  # for postgres
pip install -r requirements/mysql.txt     # for mysql, does not work with python 3.4
pip install -r requirements/test.txt      # for running tests
```

Install the client side libraries:

```
./manage.py bower install
```

Then, setup the application:

```
./manage.py migrate
./manage.py createsuperuser
```

Load the fixtures with some initial data:

```
./manage.py loaddata fixtures/domain.json
./manage.py loaddata fixtures/questions.json
./manage.py loaddata fixtures/projects.json
```

Start the development server:

```
./manage.py runserver --insecure
```

Finally, navigate to `http://locahost:8000` in your browser.


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
