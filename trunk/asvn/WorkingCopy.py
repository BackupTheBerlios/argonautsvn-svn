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
Subversion working copy.

Class representing a subversion working copy.

:authors:
    Philipp Wolfer (phw@users.berlios.de)
:copyright: 2006 Philipp Wolfer
:license: GNU General Public License
:since: 2006-11-19
:version: $Revision$
"""

from Repository import *
import os.path
import pysvn

class WorkingCopy(object):
    """
    Class representing a subversion working copy.
    
    Most of the work is done by a
    `pysvn.Client <http://pysvn.tigris.org/docs/pysvn_prog_ref.html#pysvn_client>`__
    instance. However, the WorkingCopy class provides special low level methods
    needed by the ArgonautSVN GUI classes.
    Each instance of WorkingCopy is bound to one working copy in the
    filesystem specified by the path parameter in the `__init__` method.
    
    :type path: str
    :type repository: `Repository`
    """

    def __init__(self, path):
        """
        :param path: Path to the working copy.
        :type path: str
        """
        self.__path = path
        self.__client = pysvn.Client()
        self.__client.exception_style = 1
        info = self.__client.info(path)
        self.__repository = Repository(info.url)

    def __getPath(self):
        """"""
        return self.__path
    path = property(__getPath, doc="The local path of the working copy.")
    
    def __getRepository(self):
        """"""
        return self.__repository
    repository = property(__getRepository, doc="The repository for the working copy.")
    
    def setCallbackGetLogin(self, callback):
        """
        Set a callback that is called to retrieve username and password.
        
        The callback must accept the parameters realm, username and may_save.
        It should return a tuple (retcode, username, password, may_save):
        
        retcode:
            bool, True if username and password are available, False otherwise.
        username:
            string, the username to use.
        password:
            string, the password to use.
        may_save:
            bool, True if username and password should be saved in the
            subversion configuration directory, False otherwise.
        
        Example::
        
            def get_login( realm, username, may_save ):
                return retcode, username, password, save
        
        :see: `pysvn.Client.callback_get_login <http://pysvn.tigris.org/docs/pysvn_prog_ref.html#pysvn_client_callback_get_login>`__
        :param path: Callback function.
        :type path: Callable object
        """
        self.__client.callback_get_login = callback

    def setCallbackGetLogMessage(self, callback):
        """
        Set a callback that is called to retrieve the log message if none was supplied.
        
        The callback must not expect any parameters.
        It should return a tuple (retcode, log_message):
        
        retcode:
            True, if a log message is supplied, False otherwise.
        log_message:
            string, the log message.
        
        Example::
            
            def get_log_message():
                return retcode, log_message
        
        :see: `pysvn.Client.callback_get_login <http://pysvn.tigris.org/docs/pysvn_prog_ref.html#pysvn_client_callback_get_log_message>`__
        :param path: Callback function.
        :type path: Callable object
        """
        self.__client.callback_get_log_message = callback
        
    def update(self, toRevision):
        """
        Update the working copy to the specified revision.
        
        :todo: Implement and document this method.
        """
        pass

    def commit(self, paths, logMessage):
        """Commit all paths to the repository.
        
        This method will add unversioned paths to the working copy before actual
        committing.
        
        :param paths: List of paths (string) to commit. The paths must be
            specified relative to the working copy's path.
        :type paths: list
        :param logMessage: Log message.
        :type logMessage: str
        :return: The new revision.
        :rtype: pysvn.Revision
        :see: `pysvn.Revision <http://pysvn.tigris.org/docs/pysvn_prog_ref.html#pysvn_revision>`__
        """
        # Readd working copy path to relative file paths
        paths = [os.path.join(self.path, path) for path in paths]
        
        # Add unversioned paths
        for path in paths:
            print path + '...'
            statusList = self.__client.status(path)
            for status in statusList:
                print status
                if status.text_status in [pysvn.wc_status_kind.unversioned]:
                    self.add(path)
                    break
                
        # Commit changes in selected paths
        revision = self.__client.checkin(paths,
                                         logMessage,
                                         recurse=False, keep_locks=False)
        return revision

    def add(self, path, recurse=True):
        """
        Adds the unversioned path to the working copy.
        
        :param path: Unversioned path relative to the working copy's path.
        :type path: str
        :param recurse: True, to add the path and its children recursively,
            False to add only the path itself.
        :type recurse: bool
        """
        self.__client.add(path, recurse, force=False, ignore=False)
    
    def getChangedPaths(self):
        """Return all changed paths in the working copy.
        
        Returns a list of `Entry` objects with the following fields:
        
        - path
        - rel_path
        - text_status
        
        :return: List of `Entry` objects.
        :rtype: list
        """
        changedPaths = self.__client.status(self.path,
                                            recurse = True,
                                            get_all = False,
                                            update = False,
                                            ignore = True,
                                            ignore_externals = True)
        return [Entry(self.path, entry) for entry in changedPaths]

class Entry:
    """
    :todo: Document this class.
    """
    
    def __init__(self, workingCopyPath, statusObject):
        """
        :todo: Document this method.
        """
        self.path = statusObject.path
        if workingCopyPath[-1] != '/':
            workingCopyPath = workingCopyPath + '/'
        self.rel_path = statusObject.path[len(workingCopyPath):]
        self.text_status = statusObject.text_status
        
