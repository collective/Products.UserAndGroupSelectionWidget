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

from zope.component import ComponentLookupError

from Products.CMFCore.utils import getToolByName
 
from interfaces import IGenericGroupTranslation

class MemberLookup(object):
    """This object contains the logic to list and search for users and groups.
    """
    
    def __init__(self, context, request, widget):
        """Take the current zope context as argument and construct this object.
        """
        self.context = context
        self.widget = widget
        self.searchabletext = request.get('searchabletext', '')
        group = request.get('selectgroup', '')
        try:
            grouptranslation = IGenericGroupTranslation(self.context)
            self.currentgroupid = grouptranslation.translateToRealGroupId(group)
        except ComponentLookupError:
            self.currentgroupid = group
        
    def getGroups(self):
        """Return the plone groups.
        """
        filter = self.widget.groupIdFilter
        grouptool = getToolByName(self.context, 'portal_groups')
        groups = grouptool.listGroups()
        ret = []
        for group in groups:
            gid = group.getId()
            if not self._groupIdFilterMatch(gid, filter):
                continue
            ret.append((gid, group.getGroupTitleOrName()))
        return ret
        
    def getMembers(self):
        """Return the Users of the portal in the following form.
        
        {
            'id': 'mmustermann',
            'fullname': 'Max Mustermann',
        }
        """
        group = self.currentgroupid
        st = self.searchabletext
        
        members = []
        if group != 'ignore' and group != '':
            pg = getToolByName(self.context, 'portal_groups')
            group = pg.getGroupById(group)
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
        return self._sortMembers(ret)

    def _groupIdFilterMatch(self, gid, filter):
        """
        """
        # wildcard match
        if filter.find('*') != -1:
                
            # all groups are affected
            if filter == '*':
                return True
            
            # wildcard matches like '*foo'
            elif filter.startswith('*'):
                if gid.endswith(filter[1:]):
                    return True
            
            # wildcard matches like 'foo*'
            elif filter.endswith('*'):
                if gid.startswith(filter[:-1]):
                    return True
            
            # wildacard matches like '*foo*'
            else:
                if gid.find(filter[1:-1]) != -1:
                    return True
        
        # exact match
        else:
            if filter == gid:
                return True
        
        return False
    
    def _sortMembers(self, members):
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