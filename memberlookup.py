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

import time
import types

from zope.component import ComponentLookupError

from Products.CMFCore.utils import getToolByName
 
from interfaces import IGenericGroupTranslation
from interfaces import IGenericFilterTranslation

class MemberLookup(object):
    """This object contains the logic to list and search for users and groups.
    """
    
    def __init__(self, context, request, widget):
        """Construct this object and do base initialization.
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
        except TypeError, e:
            if e[0] == 'Could not adapt':
                self.currentgroupid = group
            else:
                raise
        return            
        
    def getGroups(self):
        """Return the groups.
        """
        start = time.time()
        
        filter = self._allocateFilter()
        aclu = getToolByName(self.context, 'acl_users')
        groups = aclu.getGroups()
        ret = []
        for group in groups:
            gid = group.getId()
            if not self._groupIdFilterMatch(gid, filter):
                continue
            ret.append((gid, group.getGroupTitleOrName()))
            
        print 'getGroups took %s' % str(time.time() - start)
        
        return ret
        
    def getMembers(self):
        """Return the Users in the following form.
        
        {
            'id': 'mmustermann',
            'fullname': 'Max Mustermann',
        }
        """
        start = time.time()
        
        filter = self._allocateFilter()
        group = self.currentgroupid
        st = self.searchabletext
        aclu = getToolByName(self.context, 'acl_users')
        users = []
        user_ids = []
        if group != 'ignore' and group != '':
            group = aclu.getGroupById(group)
            if group:
                user_ids = group.getGroupMemberIds()
        else:
            # TODO: Search is done over all available groups, not only over groups which should be applied
            # also see getGroups
            if len(st) < 3:
                return []
            users_dict = aclu.searchUsers(name=st)
            user_ids = [user['id'] for user in users_dict]
        if user_ids:
            users = [aclu.getUserById(user_id) for user_id in user_ids]
        reduce = True
        for fil in filter:
            if fil == '*':
                reduce == False
        if reduce:
            users = self._reduceMembers(users, filter)
        ret = []
        for user in users:
            user_id = user.getId()
            for psheet in user.getOrderedPropertySheets():
                if psheet.hasProperty('fullname'):
                    user_fn = psheet.getProperty('fullname')
                else:
                    user_fn = user_id
            entry = {
                'id': user_id,
                'fullname': user_fn,
            }
            ret.append(entry)
        
        print 'getMembers took %s' % str(time.time() - start)
        
        return self._sortMembers(ret)
    
    def _allocateFilter(self):
        filter = self.widget.groupIdFilter
        try:
            filtertranslation = IGenericFilterTranslation(self.context)
            filter = filtertranslation.translateToFilterDefinition(filter)
        except ComponentLookupError:
            pass
        except TypeError, e:
            if e[0] == 'Could not adapt':
                pass
            else:
                raise        
        if type(filter) in types.StringTypes:
            filter = [filter,]
        return filter

    def _groupIdFilterMatch(self, gid, filter):
        """Check if gid matches filter.
        """
        for fil in filter:
            # wildcard match
            if fil.find('*') != -1:
                # all groups are affected
                if fil == '*':
                    return True
                # wildcard matches like '*foo'
                elif fil.startswith('*'):
                    if gid.endswith(fil[1:]):
                        return True
                # wildcard matches like 'foo*'
                elif fil.endswith('*'):
                    if gid.startswith(fil[:-1]):
                        return True
                # wildacard matches like '*foo*'
                else:
                    if gid.find(fil[1:-1]) != -1:
                        return True
            # exact match
            else:
                if fil == gid:
                    return True
        return False
    
    def _reduceMembers(self, members, filter):
        """Reduce members to match filter.
        """
        # TODO
        return members
    
    def _sortMembers(self, members):
        """Sort members dict alphabetically by fullname.
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