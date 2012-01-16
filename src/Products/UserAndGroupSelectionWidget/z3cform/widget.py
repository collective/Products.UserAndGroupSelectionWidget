import zope.schema
import zope.interface
import zope.component
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

import z3c.form

from Products.UserAndGroupSelectionWidget.interfaces import IGenericGroupTranslation

from interfaces import IUserAndGroupSelectionWidget
from interfaces import IUsersAndGroupsSelectionWidget

class Mixin(object):
    """ """

    @property
    def portal_type(self):
        return self.form.portal_type

    def getGroupId(self, instance):
        groupid = self.groupName
        try:
            translator = IGenericGroupTranslation(instance)
        except zope.component.ComponentLookupError:
            pass
        except TypeError, e:
            if e[0] == 'Could not adapt':
                pass
            else:
                raise TypeError(e)
        else:
            groupid = translator.translateToRealGroupId(self.groupName)
        return groupid


class UserAndGroupSelectionWidget(z3c.form.browser.text.TextWidget, Mixin):
    """ A single-valued user or group selection widget for z3c.form
    """
    zope.interface.implementsOnly(IUserAndGroupSelectionWidget)

    macro = "userandgroupselect"
    helper_js = ('userandgroupselect.js',)
    size = 8        # size of form-element taking the users
    groupName = ''  # takes the given group as default, a group id
    usersOnly = False     # only allow user selection
    groupsOnly = False    # allow only group selection
    groupIdFilter = '*'   # allow all groups
    searchableProperties = ()    # which properties you want to search as well
                                 # eg. ('email', 'fullname', 'location')

    def __init__(self, field, request):
        super(UserAndGroupSelectionWidget, self).__init__(request)


class UsersAndGroupsSelectionWidget(z3c.form.browser.multi.MultiWidget, Mixin):
    """ A multi-valued users and/or groups selection widget for z3c.form
    """
    zope.interface.implementsOnly(
                    IUsersAndGroupsSelectionWidget,
                    z3c.form.interfaces.IButtonForm, 
                    z3c.form.interfaces.IHandlerForm)

    klass = u'users-and-groups-selection-widget'
    helper_js = ('userandgroupselect.js',)
    size = 8        # size of form-element taking the users
    groupName = ''  # takes the given group as default, a group id
    usersOnly = False     # only allow user selection
    groupsOnly = False    # allow only group selection
    searchableProperties = ()   # which properties you want to search as well
                                # eg. ('email', 'fullname', 'location')

    def extract(self, default=z3c.form.interfaces.NO_VALUE):
        return self.request.get(self.name, default)

    def update(self):
        return super(z3c.form.browser.multi.MultiWidget, self).update()


@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
@zope.component.adapter(zope.schema.interfaces.IField,
                        z3c.form.interfaces.IFormLayer)
def UserAndGroupSelectionFieldWidget(field, request):
    """IFieldWidget factory for UserAndGroupSelectionWidget
    """
    return z3c.form.widget.FieldWidget(field,
        UserAndGroupSelectionWidget(field, request))

@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def UsersAndGroupsSelectionWidgetFactory(field, request):
    """IFieldWidget factory for TextLinesWidget."""
    return z3c.form.widget.FieldWidget(
                field, UsersAndGroupsSelectionWidget(request))

@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
@zope.component.adapter(zope.schema.interfaces.IField,
                        z3c.form.interfaces.IFormLayer)
def UsersAndGroupsSelectionFieldWidget(field, request):
    """IFieldWidget factory for UserAndGroupSelectionWidget
    """
    return UsersAndGroupsSelectionWidgetFactory(field, request)

