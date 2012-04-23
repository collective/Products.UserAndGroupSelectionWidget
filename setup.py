# Copyright 2008-2009, BlueDynamics Alliance, Austria - http://bluedynamics.com
# BSD derivative License 

import sys
from setuptools import setup
from setuptools import find_packages


version = '3.0b3'

if sys.version_info < (2, 7):
    extra_install_requires = ['ordereddict']
else:
    extra_install_requires = []

setup(
    name='Products.UserAndGroupSelectionWidget',
    version=version,
    description='Archetypes Widget for User and Group Selection, works '
                'with many users.',
    long_description=open('README.rst').read() + open('HISTORY.txt').read() + open('LICENSE.txt').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Zope2',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ], 
    keywords='zope zope2 plone archetypes z3cform widget user',
    author='BlueDynamics Alliance',
    author_email='dev@bluedynamics.com',
    url='https://github.com/collective/Products.UserAndGroupSelectionWidget',
    license='BSD',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages=['Products', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.interface',
        'zope.component',
        'zope.schema>=4.1.1',
        'Zope2',
        'AccessControl',
        'Products.CMFCore',
        'Products.CMFPlone',
        'Products.PlonePAS',
        'bda.cache',
        'lxml',
        'plone.dexterity',
        ] + extra_install_requires,
    extras_require = {
        'test': [
            'unittest2',
            'zope.app.testing',
            'plone.app.testing',
            ],
        },
    )
