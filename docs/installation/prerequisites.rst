Install prerequisites
---------------------

Installing the prerequisites for RDMO differs on the different operating systems and is therefore covered in different sections.

Linux
~~~~~

We recommend to install the prerequisites using the packaging system of your distribution. On debian/Ubuntu use:

.. code:: bash

    sudo apt-get install build-essential libxml2-dev libxslt-dev zlib1g-dev
    sudo apt-get install python3.5-dev                                       # for python 3
    sudo apt-get install python2.7-dev                                       # for python 2
    sudo apt-get install python-pip python-virtualenv
    sudo apt-get install git
    sudo apt-get install pandoc

    # optional, for pdf output
    sudo apt-get install texlive texlive-xetex

on RHEL/CentOS use:

.. code:: bash

    sudo yum install epel-release
    sudo yum install gcc gcc-c++ libxml2-devel libxslt-devel
    sudo yum install python-devel python-pip python-virtualenv
    sudo yum install git
    sudo yum install pandoc

    # optional, for pdf output
    sudo yum install texlive texlive-xetex texlive-mathspec texlive-euenc \
        texlive-xetex-def texlive-xltxtra

On RHEL/CentOS ``selinux`` is enabled by default. This can result in unexpected errors, depending on where you store the RDMO source code on the system. While the prefereble way is to configure it correctly (which is beyond the scope of this documentation), you can also set ``selinux`` to ``permissive`` or ``disabled`` in ``/etc/selinux/config`` (and reboot afterwards).


macOS
~~~~~

We recommend to install the prerequisites using `brew <http://brew.sh>`_:

.. code:: bash

    brew install python3                                       # for python 3
    brew install python                                        # for python 2
    brew install git
    brew install pandoc

    # optional, for pdf export
    brew install texlive

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

All further steps need to be performed using the windows shell ``cmd.exe``. You can open it from the Start-Menu.
