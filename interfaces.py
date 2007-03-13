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

from zope.interface import Interface

class IUserAndGroupSelectView(Interface):
    """
    """
    
    def initialize():
        """Initialize the view class.
        """
    
    def getObjectUrl():
        """Return the url of the current object.
        """
    
    def getQueryUrl(**kwargs):
        """Return the current query url.
        """
    
    def isSelected(param, value):
        """Return True if the given value of param was sent by the request.
        """
    
    def getGroupsForPulldown():
        """Return the plone groups.
        """
    
    def getBatch():
        """Return a AlphaBatch object.
        """
    