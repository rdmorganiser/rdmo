Setup RDMO on Windows
----------------------------

First, install the following prerequisites:

#### python

* from https://www.python.org/downloads/windows/
* we recommend a version >= 3.4
* don't forget to check 'Add Python to environment variables' during setup

#### git

* from https://git-for-windows.github.io/

#### C++ Build Tools

* from http://landinghub.visualstudio.com/visual-cpp-build-tools

#### pdflatex

* optional, for pdf export
* from http://miktex.org/

#### node.js, npm, and bower

* optional, only needed if you want to use bower to fetch the front-end components
* from https://nodejs.org/en/download/
* after the installation of node.js, install bower using `npm -g install bower` in `cmd.exe`.

To begin with the RDMO setup, open the windows shell `cmd.exe` from the Start-Menu, change to a directory of you choice, and clone the repository:

```
git clone https://github.com/rdmorganiser/rdmo
```

Change to the created directory, create a [virtualenv](https://virtualenv.readthedocs.org) and install the required python dependencies:

```
cd rdmo
python -m venv env
call env\Scripts\activate.bat

pip install -r requirements/base.txt
pip install -r requirements/development.txt  # for development
pip install -r requirements/postgres.txt     # for postgres
pip install -r requirements/mysql.txt        # for mysql
```

Download and install pandoc:

```
python -c "import pypandoc; pypandoc.download_pypandoc()"
```

Create a new file as `rdmo/settings/local.py`. You can use `rdmo/settings/sample.local.py` as template, i.e.:

```
copy rdmo\settings\sample.local.py rdmo\settings\local.py
```

Configure your database connection using the `DATABASES` variable in this file. If no `DATABASE` setting is given `sqlite3` will be used as database backend.

In addition set `DEBUG = True` for the development setup.

Then, setup the application:

```
python manage.py migrate          # initializes the database
python manage.py createsuperuser  # creates the admin user
```

Finally, install the front-end components. This can be done using bower:

```
python manage.py bower install
```

Alternatively, if node.js, npm and/or bower are not available or not wanted on the machine, download the components from

* https://github.com/rdmorganiser/rdmo-components/archive/master.zip

and extract them into `components_root` in the `rdmo` directory. In both cases a `components_root/bower_components` containing various JavaScript and CSS libraries should be available.
