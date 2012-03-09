import types
import operator

from alphabatch import AlphaBatch

from Acquisition import aq_inner
from ZTUtils import make_query

from zope.interface import implements
from zope.component import getUtility
from zope.schema.interfaces import ICollection

from z3c.form.widget import FieldWidget
from z3cform.widget import UserAndGroupSelectionWidget

from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity import utils

from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.PlonePAS.interfaces.group import IGroupIntrospection

from interfaces import IUserAndGroupSelectView
from memberlookup import MemberLookup


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
        fieldId = self.request.get('fieldId','').split('-')[-1]
        if  self.request.get('hasContentType'):
            # For contextless z3c.form forms, we can't rely on the context
            dottedname = self.request.get('dottedname')
            klass = utils.resolveDottedName(dottedname)
            field = klass(self.context, self.request).fields.get(fieldId).field
            self.widget = FieldWidget(field, UserAndGroupSelectionWidget(field, self.request))
            self.multivalued = ICollection.providedBy(field)
        else:
            context = aq_inner(self.context)
            portal_type = self.request.get('portal_type')
            if portal_type == context.portal_type and shasattr(context, 'Schema'):
                # Archetype
                field = context.Schema().getField(fieldId)
                self.multivalued = field.multiValued
                self.widget = field.widget
            else:
                # z3c.form
                fti = getUtility(IDexterityFTI, name=portal_type)
                schema = fti.lookupSchema()
                field = schema.get(fieldId)
                if field is None:
                    # The field might be defined in a behavior schema.
                    # Get the behaviors from either the context or the
                    # portal_type.
                    for behavior_schema in \
                            utils.getAdditionalSchemata(self.context, portal_type):
                        if behavior_schema is not None:
                            field = behavior_schema.get(fieldId)
                            if field is not None:
                                    break
                self.widget = FieldWidget(field, UserAndGroupSelectionWidget(field, self.request))
                self.multivalued = ICollection.providedBy(field)

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
