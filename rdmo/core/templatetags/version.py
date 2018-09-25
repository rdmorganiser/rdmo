import os
import re

from django import template
from django.apps import apps

register = template.Library()


@register.simple_tag
def version():
    init_py = os.path.join(apps.get_app_config('rdmo').path, '__init__.py')
    content = open(init_py).read()
    version = ''
    try:
        version = re.search(r'__version__.*?=.*?([0-9\.]+)', content).group(1)
    except AttributeError:
        pass
    if version != '':
        version = 'RDMO v' + version
    return version
