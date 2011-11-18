
from Products.Archetypes import atapi
from archetypes.schemaextender.field import ExtensionField
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.ATContentTypes.interface import IATDocument
from Products.UserAndGroupSelectionWidget.at import widget


class StringField(ExtensionField, atapi.StringField):
    """A string field."""

class LinesField(ExtensionField, atapi.LinesField):
    """A lines field."""



class PageExtender(object):
    adapts(IATDocument)
    implements(ISchemaExtender)


    fields = [
        StringField("field1",
            widget = widget.UserAndGroupSelectionWidget(
                label="Field1",
                ),
            ),
        LinesField("field2",
            widget = widget.UserAndGroupSelectionWidget(
                label="Field2",
                ),
            ),
        ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

