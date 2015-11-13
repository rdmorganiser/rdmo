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

Next, install create a [virtualenv](https://virtualenv.readthedocs.org) and install the required dependecies:

```
cd DMPwerkzeug
virtualenv                    env  # for python 2.7
virtualenv --python=python3.4 env  # for python 3.4
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
coverage report
coverage html
```

Then, open `htmlcov/index.html` in a browser to view the report.
All three commands are combined in the `runstest.py` script.


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
