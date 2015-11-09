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

Then, copy the `default.local.py` file:

```
cd DMPwerkzeug
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
./manage.py test --cover-html
```

Then, open `cover/index.html` in a browser to view the report.


i18n
----

To update the locale files automatiacally run:

```
./manage.py makemessages -a --ignore=compressor/* --ignore=django/*
```

Then, edit the `.po` files in the `locale` directory. Afterwards run

```
./manage.py compilemessages
```

Status
------

[![Build Status](https://travis-ci.org/DMPwerkzeug/DMPwerkzeug.svg?branch=master)](https://travis-ci.org/DMPwerkzeug/DMPwerkzeug)
