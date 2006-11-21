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

"""
:authors:
    Philipp Wolfer (phw@users.berlios.de)
:copyright: 2006 Philipp Wolfer
:license: GNU General Public License
:since: 2006-11-19
:version: $Revision$
"""

import sys
import gettext
import gtk.glade

##
# Installation prefix.
PREFIX = sys.prefix

##
# Application name used by gettext.
APP = 'argonautsvn'

##
# Locale directory.
DIR = 'locale'

gettext.install(APP, DIR, unicode=True)

gtk.glade.bindtextdomain(APP, DIR)
gtk.glade.textdomain(APP)
