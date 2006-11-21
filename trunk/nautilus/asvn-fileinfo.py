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

import nautilus
import pysvn

class ASVNFileInfo(nautilus.InfoProvider):
    """Adds SVN status emblems and column information for SVN files to nautilus.
    """
    
    emblems = {
        pysvn.wc_status_kind.none:        None,
        pysvn.wc_status_kind.unversioned: None,
        pysvn.wc_status_kind.normal:      'cvs-controlled',
                                          # cvs-added makes weird things with nautilus
        pysvn.wc_status_kind.added:       None,#'cvs-added',
        pysvn.wc_status_kind.missing:     None,
        pysvn.wc_status_kind.deleted:     'cvs-removed',
        pysvn.wc_status_kind.replaced:    None,
        pysvn.wc_status_kind.modified:    'cvs-modified',
        pysvn.wc_status_kind.merged:      None,
        pysvn.wc_status_kind.conflicted:  'cvs-conflict',
        pysvn.wc_status_kind.ignored:     None,
        pysvn.wc_status_kind.obstructed:  None,
        pysvn.wc_status_kind.external:    None,
        pysvn.wc_status_kind.incomplete:  None,
        }
    
    def __init__(self):
        print 'Initializing ArgonautSVN emblem extension'
    
    def update_file_info(self, file):
        """Updates the emblems for a file.
        
        @param[in,out] file A nautilus.FileInfo resource.
        @return None
        @todo Files should be invalidated with
        nautilus.FileInfo.invalidate_extension_info() somewhere."""
        
        print 'DEBUG: Updating file info: %s' % file.get_uri()
        if file.get_uri_scheme() != 'file':
            return
        
        path = file.get_uri()[len(file.get_uri_scheme() + '://'):]
        
        try:
            client = pysvn.Client()
            statusList = client.status(path, recurse=False)
        except pysvn.ClientError:
            return
        else:
            for status in statusList:
                emblem = ASVNEmblems.emblems[status.text_status]
                if emblem is not None:
                    file.add_emblem(emblem)
  
