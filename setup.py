from setuptools import setup, find_packages

from rdmo import __title__, __email__, __version__, __author__, __license__

setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    maintainer=__author__,
    maintainer_email=__email__,
    license=__license__,
    url='https://github.com/rdmorganiser/rdmo',
    description=u'RDMO is a tool to support the systematic planning, organisation and implementation of the data management throughout the course of a research project.',
    long_description=open('README.rst').read(),
    install_requires=[
        'Django==1.11.1',
        'djangorestframework==3.6.2',
        'drf-extensions==0.3.1',
        'django-extensions==1.7.7',
        'django-allauth==0.31.0',
        'django-filter==1.0.2',
        'django-widget-tweaks==1.4.1',
        'django-mptt==0.8.7',
        'django-compressor==2.1.1',
        'django-libsass==0.7',
        'django-settings-export==1.2.1',
        'rules==1.2',
        'jsonfield==1.0.0',
        'Markdown==2.6.8',
        'iso8601==0.1.11',
        'pypandoc==1.3.3',
        'lxml==3.7.3',
        'coverage',
        'django-test-generator>=0.3.1'
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
