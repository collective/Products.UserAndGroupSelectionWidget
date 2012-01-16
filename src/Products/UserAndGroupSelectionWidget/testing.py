from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

class UserAndGroupSelectionWidgetFixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.UserAndGroupSelectionWidget
        self.loadZCML(package=Products.UserAndGroupSelectionWidget)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'Products.UserAndGroupSelectionWidget:default')


USERANDGROUPSELECTIONWIDGET_FIXTURE = UserAndGroupSelectionWidgetFixture()
USERANDGROUPSELECTIONWIDGET_INTEGRATION_TESTING = IntegrationTesting(
    bases=(USERANDGROUPSELECTIONWIDGET_FIXTURE,),
    name="UserAndGroupSelectionWidgetFixture:Integration")

USERANDGROUPSELECTIONWIDGET_FUNCTIONAL_TESTING = \
        FunctionalTesting(
                bases=(USERANDGROUPSELECTIONWIDGET_FIXTURE,), 
                name="UserAndGroupSelectionWidgetFixture:Functional"
                )

