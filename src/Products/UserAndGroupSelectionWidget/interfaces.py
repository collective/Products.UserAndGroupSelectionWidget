from zope.interface import Interface
from plone.app.z3cform.interfaces import IPloneFormLayer

class ITestingLayer(Interface):
    """ Marker interface for requests indicating the package has been installed.
        
        This layer is only for testing purposes, (i.e to register
        schema-extenders) and has no production purpose.
    """

class ICustomFormLayer(IPloneFormLayer):
    """ Request layer installed via browserlayer.xml
    """

class IGenericGroupTranslation(Interface):
    """Utils to translate a generic name to a group name.
    """
    
    def translateToRealGroupId(genericgroup):
        """Takes generic group and translate it to a real plone group id.
        
        In case of an unmatching genericgroup this function MUST return the
        original genericgroup.
        """

class IGenericFilterTranslation(Interface):
    """Utils to translate a generic name to a group name.
    """
    
    def translateToFilterDefinition(genericfilter):
        """Takes generic filter and translate it to a real filter definition.
        
        In case of an unmatching genericfilter this function MUST return the
        original genericfilter.
        """


class IUserAndGroupSelectView(Interface):
    """View class interface for the selection popup.
    """
    
    def getUserOrGroupTitle(id):
        """Return either the fullname of the user or the grou title.
        """


class IUserAndGroupSelectPopupView(Interface):
    """View class interface for the selection popup.
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
    
    def usersOnly():
        """Return wether users only flag is set on widget or not.
        """
    
    def groupsOnly():
        """Return wether groups only flag is set on widget or not.
        """
    
    def multiValued():
        """Return wether field is multivalued or not.
        """


