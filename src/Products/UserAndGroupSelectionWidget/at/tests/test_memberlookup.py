import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from Products.UserAndGroupSelectionWidget import testing
from Products.UserAndGroupSelectionWidget.memberlookup import MemberLookup


class MemberLookupTest(unittest.TestCase):

    layer = testing.USERANDGROUPSELECTIONWIDGET_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        class FakeWidget(object):
            groupIdFilter = []
            searchableProperties = []

        self.widget = FakeWidget()
        self.widget.searchableProperties = ('email', 'fullname',
                'home_page', 'location', 'description')

        username = 'example-user'
        acl_users = getToolByName(self.portal, 'acl_users')
        acl_users.userFolderAddUser(username, 'secret', ['Member'], [])

        membership = getToolByName(self.portal, 'portal_membership')
        self.member = membership.getMemberById(username)
        self.member.setMemberProperties(mapping={
            'email': 'test@exampLe1.com',
            'fullname': 'Example2 User',
            'home_page': 'http://exaMple3.com',
            'location': 'Example4',
            'description': 'Example5 description',
            })
        self.memberlookup = MemberLookup(self.portal, self.request, self.widget)

    def test_search_user_via_username(self):
        self.memberlookup.searchabletext = 'example-'
        members = self.memberlookup.getMembers()

        self.assertEqual(1, len(members))
        self.assertEqual(self.member.getId(), members[0]['id'])

    def test_search_user_via_email(self):
        self.memberlookup.searchabletext = 'example1'
        members = self.memberlookup.getMembers()

        self.assertEqual(1, len(members))
        self.assertEqual(self.member.getId(), members[0]['id'])

    def test_search_user_via_fullname(self):
        self.memberlookup.searchabletext = 'example2'
        members = self.memberlookup.getMembers()

        self.assertEqual(1, len(members))
        self.assertEqual(self.member.getId(), members[0]['id'])

    def test_search_user_via_homepage(self):
        self.memberlookup.searchabletext = 'example3'
        members = self.memberlookup.getMembers()

        self.assertEqual(1, len(members))
        self.assertEqual(self.member.getId(), members[0]['id'])

    def test_search_user_via_location(self):
        self.memberlookup.searchabletext = 'example4'
        members = self.memberlookup.getMembers()

        self.assertEqual(1, len(members))
        self.assertEqual(self.member.getId(), members[0]['id'])

    def test_search_user_via_description(self):
        self.memberlookup.searchabletext = 'example5'
        members = self.memberlookup.getMembers()

        self.assertEqual(1, len(members))
        self.assertEqual(self.member.getId(), members[0]['id'])


    def test_disable_search_over_user_properties(self):
        self.widget.searchableProperties = ()
        memberlookup = MemberLookup(self.portal, self.request, self.widget)
        memberlookup.searchabletext = 'example1'

        self.assertEqual(0, len(memberlookup.getMembers()))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
