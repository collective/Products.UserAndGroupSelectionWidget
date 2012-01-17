import unittest
import zope.app.testing.placelesssetup
import zope.testing.doctest

def test_suite():
    return unittest.TestSuite((
            zope.testing.doctest.DocFileSuite(
                'z3cform/DOCTESTS.txt',
                package='Products.UserAndGroupSelectionWidget',
                setUp=zope.app.testing.placelesssetup.setUp,
                tearDown=zope.app.testing.placelesssetup.tearDown),
            ))
