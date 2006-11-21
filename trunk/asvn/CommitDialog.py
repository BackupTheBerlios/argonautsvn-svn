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
SVN commit dialog.

Provides a GTK based commit dialog.

:authors:
    Philipp Wolfer (phw@users.berlios.de)
:copyright: 2006 Philipp Wolfer
:license: GNU General Public License
:since: 2006-11-19
:version: $Revision$
"""

from argonautsvn import *
from WorkingCopy import *
import sys, pysvn, os.path
import threading
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk, gobject
    import gtk.glade
except:
    sys.exit(1)

class ChangedFilesThread(threading.Thread):
    """
    Thread class for generating the list of changed paths in the working copy
    in the background.
    """
    
    def __init__(self, workingCopy, callback):
        """
        :param workingCopy: Working copy for which the changed files should be
            determined.
        :type workingCopy: `asvn.WorkingCopy.WorkingCopy`
        :param callback: Callback function to run after the changed files have
            been determined. Must accept the list of changed files as a single
            parameter.
        :type callback: list
        """
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.__workingCopy = workingCopy
        self.__callback = callback

    def run(self):
        """
        Starts the thread.
        """
        threading.Thread.run(self)
        changedPaths = self.__workingCopy.getChangedPaths()
        gobject.idle_add(self.__callback, changedPaths)

class CommitDialog:
    """SVN commit dialog."""

    def __init__(self, workingCopy):
        """
        :param workingCopy: Working copy.
        :type workingCopy: `asvn.WorkingCopy.WorkingCopy`
        """
        self.workingCopy = workingCopy
     
        # Set the Glade file
        self.gladefile = os.path.join(PREFIX, 'share', APP, 'glade/commitdialog.glade')
        self.wTree = gtk.glade.XML(self.gladefile, domain=APP)
        
        # Store some important widgets
        self.window = self.wTree.get_widget('CommitDialog')
        self.textviewLogMessage = self.wTree.get_widget('textviewLogMessage')
        self.listviewChangedFiles = self.wTree.get_widget('listviewChangedFiles')
        self.warningLogMessageDialog = self.wTree.get_widget("WarningLogMessageDialog")
        self.warningLogMessageDialog.reparent(self.window)
        self.warningLogMessageDialog.set_transient_for(self.window)
        
        # Fill the list with the changed files
        self.__initChangedFilesList()
        self.thread = ChangedFilesThread(self.workingCopy, self.fillChangedFilesList)
        self.thread.start()
        
        # Connect all events
        events = {'on_CommitDialog_destroy' : self.__cancel,
                  'on_ButtonCancel_clicked' : self.__cancel,
                  'on_ButtonCommit_clicked' : self.__commit,
                  'on_ButtonLogMessageWarningOk_clicked' :
                    self.warningLogMessageDialog.hide_on_delete,
                  'on_WarningLogMessageDialog_delete_event' :
                    self.warningLogMessageDialog.hide_on_delete,
                  }
        self.wTree.signal_autoconnect(events)

        # Set callback for subversion events
        self.workingCopy.setCallbackGetLogMessage(self.__showLogMessageWarning)

        # Show main window
        self.window.show()
        
        # Don't know why, but threading won't work without those two line
        # I would have expected that the main thread of nautilus has
        # already called gobject.threads_init() before gtk.main()
        gobject.threads_init()
        gtk.main()

    def __initChangedFilesList(self):
        """Initialize the list of changed files."""
        self.changedFilesList = gtk.ListStore(bool, str, str)
        
        # Add all columns
        cellRenderer = gtk.CellRendererToggle()
        cellRenderer.set_property('activatable', True)
        cellRenderer.connect('toggled', self.__fileListToggled, self.changedFilesList)
        
        column1 = gtk.TreeViewColumn('', cellRenderer, active = 0)
        self.listviewChangedFiles.append_column(column1)

        column2 = gtk.TreeViewColumn(_(u'Status'), gtk.CellRendererText(), text = 1)
        column2.set_resizable(True)
        column2.set_sort_column_id(1)
        self.listviewChangedFiles.append_column(column2)

        column3 = gtk.TreeViewColumn(_(u'File'), gtk.CellRendererText(), text = 2)
        column3.set_resizable(True)
        column3.set_sort_column_id(2)
        self.listviewChangedFiles.append_column(column3)
        
        self.listviewChangedFiles.set_model(self.changedFilesList)

    def fillChangedFilesList(self, changedPaths):
        """
        Fill the changed files list.
        
        Callback function called by `ChangedFilesThread`.
        
        :param changedPaths: List of changed paths.
        :type changedPaths: list
        """
        print changedPaths
        for changedPath in changedPaths:
            if changedPath.text_status in (pysvn.wc_status_kind.modified,
                                           pysvn.wc_status_kind.added):
                pathStatus = True
            else:
                pathStatus = False
            entry = [pathStatus, str(changedPath.text_status), changedPath.rel_path]
            self.changedFilesList.append(entry)
        
        # Show commit button
        self.wTree.get_widget('ButtonCommit').set_sensitive(True)

    def __fileListToggled(self, cell, path, model):
        """Callback for (de)selecting files in the changed files list."""
        model[path][0] = not model[path][0]

    def __commit(self, widget):
        """Callback for the commit button.
        This method will commit all selected files using the commit message
        specified by the user."""
        textbuffer = self.textviewLogMessage.get_buffer()
        logMessage = textbuffer.get_text(textbuffer.get_start_iter(),
                                         textbuffer.get_end_iter())
        
        fileList = [file[2] for file in self.changedFilesList if file[0] == True]
        if len(fileList) > 0:
            print _(u'Committing changes...').encode('utf-8')
            try:
                revision = self.workingCopy.commit(fileList, logMessage)
            except pysvn.ClientError, e:
                try:
                    for message, code in e[1]:
                       print _(u'Error %s: %s').encode('utf-8') % (code, message)
                # Some PySVN exceptions seem to be different
                except IndexError:
                    print str(e)
            else:
                print _(u'Committed in revision %s.').encode('utf-8') % (revision.number)
                self.__closeDialog()
        else:
            print _(u'Nothing to commit').encode('utf-8')
            self.__closeDialog()

    def __showLogMessageWarning(self):
        """Displays a warning dialog if no log message was entered."""
        self.warningLogMessageDialog.show()
        return False, ""
    
    def __cancel(self, widget):
        """Callback for the cancel button."""
        print _(u'Cancel...').encode('utf-8')
        self.__closeDialog()
    
    def __closeDialog(self):
        self.window.destroy()
        self.thread.join()
        gtk.main_quit()

if __name__ == "__main__":
    wc = WorkingCopy('.')
    dialog = CommitDialog(wc)
    gtk.main()