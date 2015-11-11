DMPwerkzeug
===========

This project is currently in an early stage of development and by no means production ready.

More information will follow.


Installation
------------

First, clone the repository to a convenient place:

```
git clone https://github.com/DMPwerkzeug/DMPwerkzeug
```

Next, install create a [virtualenv](https://virtualenv.readthedocs.org) and install the required dependecies:

```
cd DMPwerkzeug
virtualenv env
source env/bin/activate

pip install -r requirements/common.txt
pip install -r requirements/postgres.txt  # for postgres
pip install -r requirements/test.txt      # for running tests
```

Then, copy the `default.local.py` file:

```
cp DMPwerkzeug/default.local.py DMPwerkzeug/local.py
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

Run the tests and create the HTML coverage report:

```
coverage run manage.py test
coverage html --omit=env/*
```

Then, open `htmlcov/index.html` in a browser to view the report.


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

Status
------

[![Build Status](https://travis-ci.org/DMPwerkzeug/DMPwerkzeug.svg?branch=master)](https://travis-ci.org/DMPwerkzeug/DMPwerkzeug)
