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
apt-get install python-dev python-pip virtualenv
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

Then, copy the `default.local.py` file:

```
cp DMPwerkzeug/settings/default.py DMPwerkzeug/settings/local.py
```

Edit your database connection in `local.py`.

Then, setup the application:

```
./manage.py migrate
./manage.py createsuperuser
```

Start the development server:

```
./manage.py runserver
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
