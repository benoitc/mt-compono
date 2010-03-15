#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from distutils.command.install_data import install_data
import os
import sys

if not hasattr(sys, 'version_info') or sys.version_info < (2, 5, 0, 'final'):
    raise SystemExit("Compono requires Python 2.5 or later.")

from setuptools import setup, find_packages
from compono import __version__

data_files = []
for root in ('compono/_design', 'compono/media', 'compono/templates'):
    for dir, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if not x.startswith('.')]
        files = [x for x in files if not x.startswith('.')]
        data_files.append((os.path.join('compono', dir),
                          [os.path.join(dir, file_) for file_ in files]))
                          
class install_package_data(install_data):
    def finalize_options(self):
        self.set_undefined_options('install',
                                   ('install_lib', 'install_dir'))
        install_data.finalize_options(self)
cmdclass = {'install_data': install_package_data }


setup(
    name = 'mtcompono',
    version = __version__,
    description = 'Minmialist Django CMS',
    long_description = file(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    author = 'Benoit Chesneau',
    author_email = 'benoitc@e-engura.org',
    license = 'BSD',
    url = 'http://github.com/benoitc/mt-compono',
    classifiers = [
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',

    ],
    
    zip_safe = False,
    packages = find_packages(),
    include_package_data = True,
    datafiles = data_files,
    cmdclass=cmdclass,
    
    install_requires = [
        'setuptools>=0.6b1'
    ],
    
    requires = [
        'django (>1.1.0)',
        'couchdbkit (>=0.4.2)',
        'simplejson (>=2.0.9)',
    ],

    test_suite = 'nose.collector',

)
