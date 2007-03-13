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

import types

from zope.interface import implements
from Products.Five import BrowserView

from ZTUtils import make_query

from interfaces import IATMemberSelectView
from memberlookup import MemberLookup
from alphabatch import AlphaBatch

class ATMemberSelectView(BrowserView):
    """See interfaces.IATMemberSelectView for documentation details.
    """
    
    implements(IATMemberSelectView)
    
    def initialize(self):
        """Initialize the view class.
        """
        self.memberlookup = MemberLookup(self.context)
        
    def getQueryUrl(self, **kwargs):
        baseUrl = self.context.absolute_url()
        if self.request.get('fieldId', '') != '':
            baseUrl += '/memberselect_popup'
        query = self._getQueryString(**kwargs)
        url = '%s?%s' % (baseUrl, query)
        return url
    
    def isSelected(self, param, value):
        param = self.request.get(param)
        if param:
            if param is types.StringType:
                param = [param]
            if value in param:
                return True
        return False
    
    def getGroupsForPulldown(self):
        ret = [('ignore', '-')]
        return ret + self.memberlookup.getGroups()
    
    def getBatch(self):
        members = self.memberlookup.getMembers(self.request)
        return AlphaBatch(members, self.context, self.request)
    
    def _getQueryString(self, **kwargs):
        params = dict()
        for key in self.request.form.keys():
            params[key] = self.request.form[key]
        params.update(kwargs)
        query = make_query(params) 
        return query