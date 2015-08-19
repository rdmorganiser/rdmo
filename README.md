DMPwerkzeug
===========

This project is currently in an early stage of development and by no means production ready.

More information will follow.


Installation
------------

First, clone the repository to ca convenient place:

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
=======

First, install [Coverage](http://nedbatchelder.com/code/coverage/):

```
pip install coverage
```

Then, run the tests and create the HTML coverage report:

```
coverage run ./manage.py test
coverage html
```

Finally, open `htmlcov/index.html` in a browser to view the report.
