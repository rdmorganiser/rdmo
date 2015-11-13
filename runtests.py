#!/usr/bin/env python
import subprocess
subprocess.call('coverage run manage.py test && coverage report && coverage html', shell=True)
