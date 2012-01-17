import logging
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName

log = logging.getLogger(__name__)

def installFormLayer(context):
    siteroot = aq_parent(context)
    portal_setup = getToolByName(siteroot, 'portal_setup')
    portal_setup.runImportStepFromProfile(
                'profile-Products.UserAndGroupSelectionWidget:default', 
                'browserlayer', 
                run_dependencies=False, 
                purge_old=None)
    log.info('Succesfully imported browserlayer.xml')
