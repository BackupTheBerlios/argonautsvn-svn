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

"""SVN credentials dialog."""

from argonautsvn import *

import os

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass

import gtk
import gtk.glade

class CredentialsDialog:
    """SVN commit dialog."""

    def __init__(self, callback, realm='', username=''):
        """The constructor."""
        self.callback = callback
        
        # Set the Glade file
        self.gladefile = os.path.join(PREFIX, 'share', APP, 'glade/credentialsdialog.glade')
        self.wTree = gtk.glade.XML(self.gladefile, domain=APP)
        
        # Store some important widgets
        self.window = self.wTree.get_widget('CredentialsDialog')
        
        # Set the correct label containing the realm
        label = self.wTree.get_widget('Label')
        label.set_text(label.get_text() % realm)
        
        # Set provided username
        self.wTree.get_widget('UsernameInput').set_text(username)
        
        # Connect all events
        events = {'on_CredentialsDialog_destroy' : self.__cancel,
                  'on_ButtonCancel_clicked' : self.__cancel,
                  'on_ButtonOk_clicked' : self.__providePassword,
                  }
        self.wTree.signal_autoconnect(events)

        # Show main window
        self.window.show()
        
        # Don't know why, but threading won't work without those two line
        # I would habe expected that the main thread of nautilus has
        # already called gobject.threads_init() before gtk.main()
        #gobject.threads_init()
        gtk.main()

    def getUsername(self):
        return self.wTree.get_widget('UsernameInput').get_text()

    def getPassword(self):
        return self.wTree.get_widget('PasswordInput').get_text()

    def __cancel(self, widget):
        """Callback for the cancel button."""
        self.__closeDialog()
        
    def __providePassword(self, widget):
        if self.callback:
            self.callback(self.getUsername(), self.getPassword())
        self.__closeDialog()
        
    def __closeDialog(self):
        self.window.destroy()
        gtk.main_quit()


if __name__ == "__main__":
    
    def testCallback(username, password):
        print 'Username: %s' % username
        print 'Password: %s' % password
    
    dialog = CredentialsDialog(testCallback, 'svn://my-repository', 'phw')