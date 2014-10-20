# -*- coding: utf-8 -*-
"""
"""
from setuptools import setup, find_packages


Name = 'pp-web-base'
ProjectUrl = ""
Version = "1.0.5"
Author = 'Edward Easton, Oisin Mulvihill'
AuthorEmail = ''
Maintainer = ''
Summary = 'Core Pyramid web package.'
License = ''
Description = Summary
ShortDescription = Summary


needed = [
    "pyramid==1.5",
    "SQLAlchemy",
    "transaction",
    "decorator",
    "pyramid_debugtoolbar",
    "pyramid_jinja2",
    "pyramid_beaker",
    "zope.sqlalchemy",
    "waitress",
    "pp-db",
    "pp-auth",
    "pp-utils",
]

test_needed = [
    "pytest-cov",
]

test_suite = 'pp.utils.tests'

EagerResources = [
    'pp',
]

ProjectScripts = [
]

PackageData = {
    '': ['*.*'],
}

EntryPoints = {
    'paste.app_factory': 'main = pp.web.base:main',
    'console': 'populate_web = pp.web.base.scripts.populate:main',
}

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
        "Topic :: Software Development :: Libraries",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    keywords='python',
    license=License,
    scripts=ProjectScripts,
    install_requires=needed,
    tests_require=test_needed,
    test_suite=test_suite,
    include_package_data=True,
    packages=find_packages(),
    package_data=PackageData,
    eager_resources=EagerResources,
    entry_points=EntryPoints,
    namespace_packages=['pp'],
)
