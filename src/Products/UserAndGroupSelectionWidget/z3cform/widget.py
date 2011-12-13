
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

    size = 8
    groupName = ''

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
                UserAndGroupSelectionWidget(request))
