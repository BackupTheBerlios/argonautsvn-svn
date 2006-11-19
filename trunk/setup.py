#!/usr/bin/env python
#
# Copyright (c) 2006 Philipp Wolfer (phw@users.berlios.de)
#
# $Id$
#
# This file is part of ArgonautSVN.
#
# ArgonautSVN is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# ArgonautSVN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ArgonautSVN; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from distutils.core import setup

import os

setup(name='ArgonautSVN',
      version='0.0.0',
      description='Nautilus Subversion extension',
      long_description='ArgonautSVN project is a Subversion client GUI implemented as an extension to Nautilus, the Gnome file manager. The project is inspired by TortoiseSVN, the SVN extension for the Windows Explorer. ArgonautSVN is intended to provide a similar powerfull SVN GUI for the Gnome desktop environment.',
      url='http://argonautsvn.berlios.de',
      author='Philipp Wolfer',
      author_email='phw@users.berlios.de',
      packages=['asvn'],
      license='GNU General Public License (GPL)',
      data_files=[
        ('share/argonautsvn/glade', [
            'share/glade/commitdialog.glade',
            'share/glade/credentialsdialog.glade',
            ]),
        ('lib/nautilus/extensions-1.0/python', [
            'nautilus/asvn-contextmenu.py',
            'nautilus/asvn-emblems.py',
            ]),
        ],
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: X11 Applications :: Gnome',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Version Control :: Subversion',
        'Topic :: Desktop Environment :: Gnome',
        ],
      )