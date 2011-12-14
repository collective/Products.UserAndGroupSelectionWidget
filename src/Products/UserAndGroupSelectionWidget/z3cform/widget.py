import z3c.form
import zope.schema
import zope.interface
import zope.component

from interfaces import IUserAndGroupSelectionWidget
from Products.UserAndGroupSelectionWidget.interfaces import IGenericGroupTranslation


class UserAndGroupSelectionWidget(z3c.form.browser.widget.HTMLTextInputWidget,
                                  z3c.form.widget.Widget):
    """ User and Groups selection widget for z3c.form
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
        if hasattr(request.get('PUBLISHED'), 'form_instance'):
            # This feels very fragile, but I don't know how else to do this
            z3cform = request['PUBLISHED'].form_instance
            self.portal_type = z3cform.portal_type
        else:
            self.portal_type = None

        super(UserAndGroupSelectionWidget, self).__init__(request)

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
                raise
        else:
            groupid = translator.translateToRealGroupId(self.groupName)
        return groupid


@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
@zope.component.adapter(zope.schema.interfaces.IField,
                        z3c.form.interfaces.IFormLayer)
def UserAndGroupSelectionFieldWidget(field, request):
    """IFieldWidget factory for UserAndGroupSelectionWidget
    """
    return z3c.form.widget.FieldWidget(field,
        UserAndGroupSelectionWidget(field, request))

