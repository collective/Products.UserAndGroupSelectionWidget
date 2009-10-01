from widget import UserAndGroupSelectionWidget
from interfaces import IGenericGroupTranslation
from interfaces import IGenericFilterTranslation

from Products.CMFCore.DirectoryView import registerDirectory
from config import GLOBALS
registerDirectory('skins', GLOBALS)
