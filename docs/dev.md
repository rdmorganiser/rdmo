Development setup
=================

Install prerequisites
---------------------

Install the prerequisites for your Linux distribution as described [in the documentation](https://rdmo.readthedocs.io/en/latest/installation/prerequisites.html).


Obtain repositories
-------------------

First create a directory called `rdmorganiser` somewhere where you usually put your coding projects.

```bash
mkdir path/to/rdmorganiser
cd path/to/rdmorganiser
```

Next clone the `rdmo-app` and the `rdmo` repositories from GitHub. If you have an account there, and added your public ssh key you can use:

```bash
git clone git@github.com:rdmorganiser/rdmo-app
git clone git@github.com:rdmorganiser/rdmo
```

Otherwise you can clone the repos using:

```bash
git clone https://github.com/rdmorganiser/rdmo-app
git clone https://github.com/rdmorganiser/rdmo
```

You should now have two directories in `rdmorganiser`: `rdmo` and `rdmo-app`.


Setup rdmo-app
--------------

Change into `rdmo-app` and create a Python virtual environment:

```bash
cd path/to/rdmorganiser/rdmo-app
python3 -m venv env
source env/bin/activate                     # on Linux or macOS
call env\Scripts\activate.bat               # on Windows
pip install --upgrade pip setuptools        # update pip and setuptools
```

Install `rdmo` in *editable* mode:

```
pip install -e ../rdmo
```

This links the cloned `rdmo` repo in a way that changes to the code will be available to the development server instantly.

If you want to use PostgreSQL or MySQL for the development you need to install the Python dependencies for this as well.

```
pip install -r requirements/postgres.txt
pip install -r requirements/mysql.txt
```

Create a `local.py`:

```bash
cp config/settings/sample.local.py config/settings/local.py
```

In the new file, set `DEBUG = True` and configure the `DATABASE` entry. The simplest way is to use Sqlite3:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
```

Then, initialize the application, using:

```bash
python manage.py download_vendor_files  # download front-end vendor files
python manage.py migrate                # initializes the database
python manage.py setup_groups           # creates groups with different permissions
```

The testing data can be imported using:

```bash
python manage.py loaddata ../rdmo/testing/fixtures/*
```
To update the testing data fixtures based on the current database, each of the RDMO apps with new data needs to be dumped using the following command.
As an example, the views and projects app contain new data:
```bash
python manage.py dumpdata --indent 4 -o ../rdmo/testing/fixtures/views.json views
python manage.py dumpdata --indent 4 -o ../rdmo/testing/fixtures/projects.json projects
```

The test upload files are initialized using:

```bash
cp -r ../rdmo/testing/media media_root
```

Starting from RDMO `1.10.0` we use [webpack](https://webpack.js.org/) to bundle the new React based front-end. For this [nodejs](https://nodejs.org) needs to be available. The prefered way is to use [nvm.sh](https://github.com/nvm-sh/nvm). It can be installed for the current user with:

```
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
```

After the installation add:

```
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

to your to your `.bashrc`. Then run:

```
nvm install    # only once, to install the node version given in .nvmrc
nvm use        # to activate the node version
npm install    # to install the many, many javascript dependencies
npm run watch  # to build the fornt-end and rebuild it when changing the source
```

Now the development server can be started (in a different terminal) using:

```
python manage.py runserver
```

You can access the application at http://localhost:8000 in your browser and can login using different users:

```plain
admin    -> superuser
site     -> site manager

editor   -> member of the editor group
reviewer -> member of the reviewer group
api      -> member of the api group

owner    -> owner of the test projects
manager  -> manager of the test projects
author   -> author of the test projects
guest    -> guest of the test projects

user     -> user without project
other    -> another user without project
```

The password for these users is the same as the username, e.g. `admin`: `admin`. You might have guessed yourself, but make sure to **never use these users in a production environment**.


Setup rdmo
----------

In order to run the test suite, the `rdmo` repo itself can be setup in a similar way in its own virtual environment:

```
deactivate                                  # if you are allready in an env
cd path/to/rdmorganiser/rdmo
python3 -m venv env
source env/bin/activate                     # on Linux or macOS
call env\Scripts\activate.bat               # on Windows
pip install --upgrade pip setuptools        # update pip and setuptools
```

Again install `rdmo` in editable mode and install the database prerequisites:

```
pip install -e .

pip install psycopg2-binary                 # for PostgreSQL
pip install mysqlclient                     # for MySQL
```

Create a `local.py` as before, but this time in `testing/config/settings/local.py`:

```bash
cp testing/config/settings/sample.local.py testing/config/settings/local.py
```

Create a log directory:

```bash
mkdir testing/log
```

Now you can run the test using:

```
pytest
```

More about testing can be found [here](testing.md).


Setup plugins
-------------

In order to include plugins into the development setup simply clone the plugin repository next to `rdmo` and `rdmo-app`, e.g. for `rdmo-plugins`:

```bash
git clone git@github.com:rdmorganiser/rdmo-plugins      # over ssh
git clone https://github.com/rdmorganiser/rdmo-plugins  # over https
```

Then the plugin can be added to the `env` for `rdmo-app` or `rdmo` also in *editable* mode using:

```bash
pip install -e ../rdmo-plugins
```

The plugin itself needs to be added to the `local.py` as described [in the documentation](https://rdmo.readthedocs.io/en/latest/plugins/index.html).
