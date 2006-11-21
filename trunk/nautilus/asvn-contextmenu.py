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

import os
import nautilus
import pysvn

from asvn.argonautsvn import *
from asvn.CommitDialog import *
from asvn.WorkingCopy import *

def get_file_directory(file):
    """Returns the directory path a file resides in.
    Will return the parent directory for files and the
    directory itself for directories."""
    if file.is_directory():
        path = file.get_uri()
    else:
        path = file.get_parent_uri()
    return path[len(file.get_uri_scheme() + '://'):]

class ASVNContextMenu(nautilus.MenuProvider):
    def __init__(self):
        print 'Initializing ArgonautSVN context menu extension'
    
    def menu_activate_cb(self, menu, file):
        pass
    
    def menu_background_activate_cb(self, menu, file):
        path = get_file_directory(file)
        workingCopy = WorkingCopy(path)
        commitDialog = CommitDialog(workingCopy)
       
    def get_file_items(self, window, files):
        if not files:
            return None
        
        itemList = []        
        
        # One single file should behave like a click in the background
        if len(files) == 1:
            itemList = self.get_background_items(window, files[0])
        else:
            # Multiple files...
            pass
        
        return itemList

    def get_background_items(self, window, file):
        itemList = []
        
        if self.is_versioned(file):
            item = nautilus.MenuItem('asvn::commit',
                                     _(u'Commit changes'),
                                     _(u'Commit changes to subverson repository'))
            item.connect('activate', self.menu_background_activate_cb, file)
            itemList.append(item)
            
            #item = nautilus.MenuItem('asvn::update',
            #                         _(u'Update'),
            #                         _(u'Update working copy'))
            #item.connect('activate', self.menu_background_activate_cb, file)
            #itemList.append(item)
            
        return itemList
        
    def is_versioned(self, file):
        """Checks if file is under Subversion version control.
        Return True if it is, False otherwise."""
        if file.get_uri_scheme() != 'file':
            return False
        
        path = get_file_directory(file)
            
        try:
            client = pysvn.Client()
            info = client.info(path)
        except pysvn.ClientError:
            return False
        else:
            return info != None and True or False
