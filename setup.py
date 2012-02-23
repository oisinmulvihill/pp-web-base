# -*- coding: utf-8 -*-
"""
Setuptools script for pp-bookingsys-web (pp.bookingsys.web)

"""

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

Name='pp-bookingsys-web'
ProjectUrl=""
Version="1.0.dev1"
Author=''
AuthorEmail='everyone at pythonpro dot co dot uk'
Maintainer=''
Summary=' pp-bookingsys-web '
License=''
Description=Summary
ShortDescription=Summary

needed = [
    'nose',
    'evasion-common',
    'sphinx', # for docs generation.
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'pyramid_jinja2',
    'pyramid_beaker',
    'zope.sqlalchemy',
    'waitress',
]

test_needed = [
]

test_suite = 'pp.bookingsys.web.tests'

EagerResources = [
    'pp',
]

# Example including shell script out of scripts dir
ProjectScripts = [
#    'pp.bookingsys.web/scripts/somescript',
]

PackageData = {
    '': ['*.*'],
}

# Example console script and paster template integration:
EntryPoints = """
[paste.app_factory]
      main = pp.bookingsys.web:main
[console_scripts]
      populate_web = pp.bookingsys.web.scripts.populate:main
"""

setup(
    url=ProjectUrl,
    name=Name,
    zip_safe=False,
    version=Version,
    author=Author,
    author_email=AuthorEmail,
    description=ShortDescription,
    long_description=Description,
    classifiers=[
      "Programming Language :: Python",
      "Framework :: Pylons",
      "Topic :: Internet :: WWW/HTTP",
      "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    keywords='web wsgi bfg pylons pyramid',
    license=License,
    scripts=ProjectScripts,
    install_requires=needed,
    tests_require=test_needed,
    test_suite=test_suite,
    include_package_data=True,
    packages=find_packages(),
    package_data=PackageData,
    eager_resources = EagerResources,
    entry_points = EntryPoints,
    namespace_packages = ['pp', 'pp.bookingsys'],
)
