import types
import operator

from Products.Five import BrowserView
from Products.PlonePAS.interfaces.group import IGroupIntrospection
from Products.CMFCore.utils import getToolByName
from ZTUtils import make_query
from z3c.form.widget import FieldWidget
from zope.interface import implements

from interfaces import IUserAndGroupSelectView
from memberlookup import MemberLookup
from alphabatch import AlphaBatch
from z3cform.widget import UserAndGroupSelectionWidget


class UserAndGroupSelectView(BrowserView):
    """See interfaces.IUserAndGroupSelectView for documentation details.
    """

    def getUserOrGroupTitle(self, id):
        pas = getToolByName(self.context, 'acl_users')
        user = pas.getUserById(id)

        if user is not None:
            fullname = self._getPropertyForMember(user, 'fullname')
            return fullname or id

        for pluginid, plugin in pas.plugins.listPlugins(IGroupIntrospection):
            group = plugin.getGroupById(id)
            if group is not None:
                title = self._getPropertyForMember(group, 'title')
                return title or id

        return id

    def _getPropertyForMember(self, member, propertyname):
        propsheets = member.listPropertysheets()
        for propsheettitle in propsheets:
            propsheet = member.getPropertysheet(propsheettitle)
            property = propsheet.getProperty(propertyname, None)
            if property:
                return property

        return None


class UserAndGroupSelectPopupView(BrowserView):
    """See interfaces.IUserAndGroupSelectPopupView for documentation details.
    """

    implements(IUserAndGroupSelectView)

    def initialize(self):
        """Initialize the view class."""
        fieldId = self.request['fieldId']
        fieldIds = fieldId.split('-')
        field = self.context

        # figure out widget type
        if getattr(field, 'Schema', None) is not None:
            # compoundfield and arrayfield compatibility
            for fieldId in fieldIds:
                field = field.Schema().getField(fieldId)
            self.multivalued = field.multiValued
            self.widget = field.widget
        else:
            # z3c.form
            # TODO: replace following two lines with code to lookup form through it's name or something
            from z3cform.tests.form import TestForm
            form = TestForm(self.context, self.request)
            field = form.fields[fieldIds[-1]]
            self.widget = FieldWidget(field.field, UserAndGroupSelectionWidget(self.request))

            # ugly hack to check if field is multivalued since z3c.form does not provide the check atm
            o = field.field._type
            self.multivalued = hasattr(o, '__len__') and hasattr(o, '__iter__') and not isinstance(o, basestring)

        self.memberlookup = MemberLookup(self.context,
                                         self.request,
                                         self.widget)

    def getObjectUrl(self):
        r = '%s/%s' % (self.context.absolute_url(), 'userandgroupselect_popup')
        return r

    def getQueryUrl(self, **kwargs):
        baseUrl = self.context.absolute_url()
        if self.request.get('fieldId', '') != '':
            baseUrl += '/userandgroupselect_popup'
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
        groups = self.memberlookup.getGroups()
        return ret + sorted(groups, key=operator.itemgetter(1))

    def getBatch(self):
        members = self.memberlookup.getMembers()
        return AlphaBatch(members, self.context, self.request)

    def usersOnly(self):
        return self.widget.usersOnly

    def groupsOnly(self):
        return self.widget.groupsOnly

    def multiValued(self):
        if self.multivalued:
            return 1
        return 0

    def _getQueryString(self, **kwargs):
        params = dict()
        for key in self.request.form.keys():
            params[key] = self.request.form[key]
        params.update(kwargs)
        query = make_query(params)
        return query
