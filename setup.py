import re

from setuptools import setup, find_packages

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
        'Django>=1.11,<2',
        'djangorestframework>=3.7',
        'drf-extensions>=0.3',
        'django-extensions>=1.7',
        'django-allauth>=0.31',
        'django-filter>=1.1,<2',
        'django-widget-tweaks>=1.4',
        'django-mptt>=0.8',
        'django-compressor>=2.2',
        'django-libsass==0.7',
        'django-settings-export>=1.2',
        'rules>=1.2',
        'jsonfield>=1.0',
        'Markdown>=2.6',
        'iso8601>=0.1',
        'pypandoc>=1.3',
        'defusedxml==0.5.0',
        'coverage>=4.5',
        'django-test-generator>=0.3.1',
        'django-rest-swagger==2.2.0'
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
