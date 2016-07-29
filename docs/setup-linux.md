Setup RDMO on Linux
-------------------

First, install a few prerequisites using your distributions packaging system. On debian/Ubuntu use:

```
sudo apt-get install git
sudo apt-get install npm nodejs-legacy
sudo apt-get install python-dev python-pip virtualenv
sudo apt-get install libxml2-dev libxslt-dev
sudo apt-get install pandoc
sudo apt-get install texlive                               # for pdf output
```

on RHEL/Centos use:

```
sudo yum install epel-release
sudo yum install git
sudo yum install npm
sudo yum install python-devel python-pip python-virtualenv
sudo yum install libxml2-devel libxslt-devel
sudo yum install pandoc
sudo yum install texlive                                   # for pdf output
```

Then install `bower` using npm:

```
sudo npm -g install bower
```

Now, clone the repository to a convenient place:

```
git clone https://github.com/rdmorganiser/rdmo
```

Change to the created directory, create a [virtualenv](https://virtualenv.readthedocs.org) and install the required dependecies:

```
cd rdmo
virtualenv env                     # for python 2.7
python -m venv env                 # for python 3.4
source env/bin/activate

pip install -r requirements/base.txt
pip install -r requirements/postgres.txt  # for postgres
pip install -r requirements/mysql.txt     # for mysql, does not work with python 3.4
pip install -r requirements/test.txt      # for running tests
```

Create a new file as `rdmo/settings/local.py`. You can use `rdmo/settings/development.py` or `rdmo/settings/production.py` as template, i.e.:

```
cp rdmo/settings/development.py rdmo/settings/local.py
```

Install the client side libraries using `bower`:

```
./manage.py bower install
```

Configure your database connection using the `DATABASES` variable in this file. If no `DATABASE` setting is given `sqlite3` will be used as database backend.

In addition set `DEBUG = True` for the development setup.

Then, setup the application:

```
./manage.py migrate          # initializes the database
./manage.py createsuperuser  # creates the admin user
```
