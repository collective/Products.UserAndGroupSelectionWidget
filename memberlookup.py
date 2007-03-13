# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Robert Niederreiter <robertn@bluedynamics.com>"""
__docformat__ = 'plaintext'

from Products.CMFCore.utils import getToolByName

class MemberLookup(object):
    """This object contains the logic to list and search for users and groups.
    """
    
    def __init__(self, context):
        """Take the current zope context as argument and construct this object.
        """
        self.context = context
    
    def getGroups(self):
        """Return the plone groups.
        """
        grouptool = getToolByName(self.context, 'portal_groups')
        groups = grouptool.listGroups()
        ret = []
        for group in groups:
            ret.append((group.getId(), group.getGroupTitleOrName()))
        return ret
        
    def getMembers(self, request):
        """Return the Users of the portal in the following form.
        
        {
            'id': 'mmustermann',
            'fullname': 'Max Mustermann',
        }
        """
        ag = request.get('selectgroup', '')
        st = request.get('searchabletext', '')
        
        members = []
        if ag != 'ignore' and ag != '':
            pg = getToolByName(self.context, 'portal_groups')
            group = pg.getGroupById(ag)
            members = group.getGroupMembers()
        else:
            if len(st) < 3:
                return []
            pm = getToolByName(self.context, 'portal_membership')
            # dirty
            members = pm.searchForMembers({'name': st})
        
        ret = []
        for member in members:
            entry = {
                'id': member.getId(),
                'fullname': member.getProperty('fullname', ''),
            }
            ret.append(entry)
        return self.sortMembers(ret)
    
    def sortMembers(self, members):
        """Sort entries.
        """
        names = []
        tmp = {}
        for member in members:
            fullname = member['fullname'].lower()
            inUse = True
            p = 1
            while inUse:
                if fullname in tmp.keys():
                    fullname = fullname + str(p)
                    p += 1
                else:
                    inUse = False
            names.append(fullname)
            tmp[fullname] = member
        names.sort()
        ret = []
        for name in names:
            ret.append(tmp[name])
        return ret