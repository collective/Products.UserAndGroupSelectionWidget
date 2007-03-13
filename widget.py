# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 by BlueDynamics Alliance, Austria
#
# major parts of this code are derived from ATMemberselectWidget
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
__author__ = """Jens Klein <jens@bluedynamics.com>"""
__docformat__ = 'plaintext' 

import types
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.utils import shasattr

class UserAndGroupSelectionWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro'         : "userandgroupselection",
        'helper_js'     : ('userandgroupselection.js',),
        'size'          : 10,    # size of form-element taking the users
        'fieldType'     : 'id',  # ['nameemail'|'email'|'id']
        'groupName'     : '',    # takes the given group as default
        'limitToGroup'  : True,  # only allow users from groupName
        'groupsOnly'    : False, # only allow to select groups
        'usersOnly'     : False, # only allow to select users
        'enableSearch'  : 1,     # enable search for userid, fullname or email
        'close_window'  : -1,    # auto close window after user is selected 
        'show_fullname' : 0,     # show fullname instead of user id in the 
                                 # widget view macro
        'link_to_home'  : 0,     # show_fullname if set, member id/fullname in 
                                 # view macro will be hyperlink to member's home folder
        })

    security = ClassSecurityInfo()    

    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None, emptyReturnsMarker=None,):
        """process the form data and return it."""
        result = TypesWidget.process_form (self, instance, field, form, 
                                           empty_marker, emptyReturnsMarker, )
        if result is empty_marker:
            return result
        value, kwargs = result
        
        # The widget always returns a empty item (strange) when we use the multival option.
        # Remove the empty items manually
        if type(value) is types.ListType:
            value = [item for item in value if item]

        return value, kwargs

registerWidget(UserAndGroupSelectionWidget,
               title='User and Group Selection Widget',
               description=('You can select users searched from a popup window.'),
               used_for=('Products.Archetypes.Field.LinesField',
	                     'Products.Archetypes.Field.StringField', )
               )
