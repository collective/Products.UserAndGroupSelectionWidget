from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from Products.ATContentTypes.interface import IATDocument
from Products.Archetypes import atapi
from Products.UserAndGroupSelectionWidget.interfaces import ITestingLayer
from Products.UserAndGroupSelectionWidget.at import widget

class StringField(ExtensionField, atapi.StringField):
    """A string field."""

class LinesField(ExtensionField, atapi.LinesField):
    """A lines field."""

class PageExtender(object):
    adapts(IATDocument)
    layer = ITestingLayer
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)

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

