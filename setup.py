import re

from setuptools import find_packages, setup

# get metadata from mudule using a regexp
with open('rdmo/__init__.py') as f:
    metadata = dict(re.findall(r'__(.*)__ = [\']([^\']*)[\']', f.read()))

setup(
    name=metadata['title'],
    version=metadata['version'],
    author=metadata['author'],
    author_email=metadata['email'],
    maintainer=metadata['author'],
    maintainer_email=metadata['email'],
    license=metadata['license'],
    url='https://github.com/rdmorganiser/rdmo',
    description=u'RDMO is a tool to support the systematic planning, organisation and implementation of the data management throughout the course of a research project.',
    long_description=open('README.rst').read(),
    install_requires=[
        'Django>=2.2.1',
        'djangorestframework>=3.9.4',
        'drf-extensions>=0.5.0',
        'django-extensions>=2.1.7',
        'django-allauth>=0.39.1',
        'django-filter>=2.1.0',
        'django-widget-tweaks>=1.4.3',
        'django-mptt>=0.10.0',
        'django-compressor>=2.2',
        'django-libsass>=0.7',
        'django-settings-export>=1.2.1',
        'rules>=2.0.1',
        'jsonfield>=1.0',
        'Markdown>=3.1',
        'iso8601>=0.1.12',
        'pypandoc>=1.4',
        'defusedxml>=0.6.0',
        'coverage>=4.5.3',
        'django-test-generator>=0.6',
        'django-rest-swagger>=2.2.0'
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'
    ],
    packages=find_packages(),
    include_package_data=True
)
