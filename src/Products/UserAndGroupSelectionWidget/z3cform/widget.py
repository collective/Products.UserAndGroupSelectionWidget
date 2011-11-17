
import z3c.form
import zope.schema
import zope.interface
import zope.component

from interfaces import IUserAndGroupSelectionWidget


class UserAndGroupSelectionWidget(z3c.form.browser.widget.HTMLTextInputWidget,
                                  z3c.form.widget.Widget):
    """ User and Groups selection widget for z3c.form
    """

    zope.interface.implementsOnly(IUserAndGroupSelectionWidget)


@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
@zope.component.adapter(zope.schema.interfaces.IField,
                        z3c.form.interfaces.IFormLayer)
def UserAndGroupSelectionFieldWidget(field, request):
    """IFieldWidget factory for UserAndGroupSelectionWidget
    """
    return z3c.form.widget.FieldWidget(field,
                UserAndGroupSelectionWidget(request))


