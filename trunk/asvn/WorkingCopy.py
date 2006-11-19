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

"""Class representing a subversion working copy."""

from Repository import *
import os.path
import pysvn

class WorkingCopy:
    """Class representing a subversion working copy.
    Most of the work is done by a pysvn.Client instance.
    However, the WorkingCopy class provides special low level methods
    needed by the ArgonautSVN GUI classes.
    Each instance of WorkingCopy is bound to one working copy in the
    filesystem specified by the path parameter in the __init__ method.
    """

    def __init__(self, path):
        self.path = path
        self.client = pysvn.Client()
        self.client.exception_style = 1
        info = self.client.info(path)
        self.repository = Repository(info.url)

    def getPath(self):
        return self.path

    def getRepository(self):
        """Returns a Repository instance."""
        return self.repository
    
    def setCallbackGetLogin(self, callback):
        self.client.callback_get_login = callback

    def setCallbackGetLogMessage(self, callback):
        self.client.callback_get_log_message = callback
        
    def update(self, toRevision):
        pass

    def commit(self, paths, logMessage):
        """Commit all paths.
        Returns the new revision on success."""
        # Readd working copy path to relative file paths
        paths = [os.path.join(self.path, path) for path in paths]
        
        # Add unversioned paths
        for path in paths:
            print path + '...'
            statusList = self.client.status(path)
            for status in statusList:
                print status
                if status.text_status in [pysvn.wc_status_kind.unversioned]:
                    self.add(path)
                    break
                
        # Commit changes in selected paths
        revision = self.client.checkin(paths,
                                       logMessage,
                                       recurse=False, keep_locks=False)
        return revision

    def add(self, path, recurse=True):
        self.client.add(path, recurse, force=False, ignore=False)
    
    def getChangedPaths(self):
        """Return all changed paths in the working copy.
        Returns a list of Entry objects with the following fields:
        - path
        - rel_path
        - text_status
        """
        changedPaths = self.client.status(self.path,
                                          recurse = True,
                                          get_all = False,
                                          update = False,
                                          ignore = True,
                                          ignore_externals = True)
        return [Entry(self.path, entry) for entry in changedPaths]

class Entry:
    def __init__(self, workingCopyPath, statusObject):
        self.path = statusObject.path
        if workingCopyPath[-1] != '/':
            workingCopyPath = workingCopyPath + '/'
        self.rel_path = statusObject.path[len(workingCopyPath):]
        self.text_status = statusObject.text_status
        
