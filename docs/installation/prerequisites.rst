Install prerequisites
---------------------

Installing the prerequisites for RDMO differs on the different operating systems and is therefore covered in different subsections.

Linux
~~~~~

We recommend to install the prerequisites using the packaging system of your distribution. On debian/Ubuntu use:

.. code:: bash

    sudo apt-get install git
    sudo apt-get install python-dev python-pip python-virtualenv
    sudo apt-get install libxml2-dev libxslt-dev
    sudo apt-get install pandoc

    # optional, for pdf output
    sudo apt-get install texlive

    # optional, to use bower to fetch front-end components
    sudo apt-get install nodejs nodejs-legacy npm
    sudo npm -g install bower

on RHEL/CentOS use:

.. code:: bash

    sudo yum install epel-release
    sudo yum install git
    sudo yum install python-devel python-pip python-virtualenv
    sudo yum install libxml2-devel libxslt-devel
    sudo yum install pandoc

    # optional, for pdf output
    sudo yum install texlive

    # optional, to use bower to fetch front-end components
    sudo yum install nodejs
    sudo npm install -g bower

On RHEL/CentOS ``selinux`` is enabled by default. This can result in unexpected errors, depending on where you store the RDMO source code on the system. While the prefereble way is to configure it correctly (which is beyond the scope of this documentation), you can also set ``selinux`` to ``permissive`` or ``disabled`` in ``/etc/selinux/config`` (and reboot afterwards).


macOS
~~~~~

We recommend to install the prerequisites using `brew <http://brew.sh>`_:

.. code:: bash

    brew install python                                        # for python 2.7
    brew install python3                                       # for python 3.4
    brew install git
    brew install pandoc

    # optional, for pdf export
    brew install texlive

    # optional, to use bower to fetch front-end components
    brew install node
    npm -g install bower

Windows
~~~~~~~

On Windows, the software prerequisites need to be downloaded and installed from their particular web sites.

For python:

* download from https://www.python.org/downloads/windows/
* we recommend a version >= 3.4
* don't forget to check 'Add Python to environment variables' during setup

For git:

* download from https://git-for-windows.github.io/

For the Microsoft C++ Build Tools:

* download from http://landinghub.visualstudio.com/visual-cpp-build-tools

For pdflatex (optional, for pdf export):

* download from http://miktex.org/

For node.js, npm, and bower (optional, only needed if you want to use bower to fetch the front-end components):

* download from https://nodejs.org/en/download/
* after the installation of node.js, install bower using ``npm -g install bower`` in ``cmd.exe``.

All further steps need to be performed using the windows shell ``cmd.exe``. You can open it from the Start-Menu.
