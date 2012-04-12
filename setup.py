# -*- coding: utf-8 -*-
"""
Setuptools script for pp-web-base (pp.web.base)

"""

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

Name='pp-web-base'
ProjectUrl=""
Version="1.0.dev1"
Author=''
AuthorEmail='everyone at pythonpro dot co dot uk'
Maintainer=''
Summary=' pp-web-base '
License=''
Description=Summary
ShortDescription=Summary

needed = [
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
    'pp-common-db',
    'pp-auth',
]

test_needed = [
]

test_suite = 'pp.web.base.tests'

EagerResources = [
    'pp',
]

# Example including shell script out of scripts dir
ProjectScripts = [
#    'pp.web.base/scripts/somescript',
]

PackageData = {
    '': ['*.*'],
}

# Example console script and paster template integration:
EntryPoints = """
[paste.app_factory]
      main = pp.web.base:main
[console_scripts]
      populate_web = pp.web.base.scripts.populate:main
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
    namespace_packages = ['pp', 'pp.web'],
)
