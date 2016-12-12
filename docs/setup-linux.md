Setup RDMO on Linux
-------------------

First, install a few prerequisites using your distributions packaging system. On debian/Ubuntu use:

```
sudo apt-get install git
sudo apt-get install python-dev python-pip virtualenv
sudo apt-get install libxml2-dev libxslt-dev
sudo apt-get install pandoc

# optional, for pdf output
sudo apt-get install texlive

# optional, to use bower to fetch front-end components
sudo apt-get install nodejs nodejs-legacy npm
npm -g install bower
```

on RHEL/Centos use:

```
sudo yum install epel-release
sudo yum install git
sudo yum install python-devel python-pip python-virtualenv
sudo yum install libxml2-devel libxslt-devel
sudo yum install pandoc

# optional, for pdf output
sudo yum install texlive

# optional, to use bower to fetch front-end components
sudo yum install nodejs
npm install -g bower
```

Now, clone the repository to a convenient place:

```
git clone https://github.com/rdmorganiser/rdmo
```

Change to the created directory, create a [virtualenv](https://virtualenv.readthedocs.org) and install the required dependecies:

```
cd rdmo
virtualenv env                               # for python 2.7
python -m venv env                           # for python 3.4
source env/bin/activate

pip install -r requirements/base.txt
pip install -r requirements/development.txt  # for development
pip install -r requirements/postgres.txt     # for postgres
pip install -r requirements/mysql.txt        # for mysql
```

Create a new file as `rdmo/settings/local.py`. You can use `rdmo/settings/sample.local.py` as template, i.e.:

```
cp rdmo/settings/sample.local.py rdmo/settings/local.py
```

Configure your database connection using the `DATABASES` variable in this file. If no `DATABASE` setting is given `sqlite3` will be used as database backend.

In addition set `DEBUG = True` for the development setup.

Then, setup the application:

```
./manage.py migrate          # initializes the database
./manage.py createsuperuser  # creates the admin user
```

Finally, install the front-end components. This can be done using bower:

```
python manage.py bower install
```

Alternatively, if node.js, npm and/or bower are not available or not wanted on the machine, download the components using `wget`:

```
wget -qO- https://github.com/rdmorganiser/rdmo-components/archive/master.tar.gz | tar xvz
mv rdmo-components-master components_root
```

In both cases a `components_root/bower_components` containing various JavaScript and CSS libraries should be available.
